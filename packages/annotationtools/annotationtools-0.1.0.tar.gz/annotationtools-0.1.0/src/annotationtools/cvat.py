# Copyright 2021-2023
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from copy import copy
from io import StringIO
import logging
from typing import IO, Union
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET

from dateutil.parser import parse as date_parse
from shapely.geometry import box, Polygon, LineString, Point, MultiPoint
import shapely

from .dataset import Annotation, Frame, Dataset, User, Label, LabelType, Attribute, InputType

def _get_text_val(tag: Element, path: str) -> str:
    sub = tag.find(path)
    if sub is not None:
        if sub.text is not None:
            return sub.text.strip()

    return None


def _parse_meta(d: Dataset, root: Element):
    job = root.find('./meta/job')
    if job is not None:
        d.id = _get_text_val(job, './id')
        d.name = _get_text_val(job, './name')
        d.size = int(_get_text_val(job, './size'))
        d.mode = _get_text_val(job, './mode')
        d.overlap = int(_get_text_val(job, './overlap'))
        d.bugtracker = _get_text_val(job, './bugtracker')
        d.subset = _get_text_val(job, './subset')

        try:
            d.created = date_parse(_get_text_val(job, './created'))
        except:
            pass

        try:
            d.updated = date_parse(_get_text_val(job, './updated'))
        except:
            pass

        owner_username = _get_text_val(job, './owner/username')
        owner_email = _get_text_val(job, './owner/email')

        if owner_username is not None:
            d.owner = User(owner_username, owner_email)


def _parse_labels(d: Dataset, root: Element):
    for label in root.findall('./meta/job/labels/label'):
        name = _get_text_val(label, './name')

        label_type = None
        try:
            label_type_str = _get_text_val(label, './type')
            label_type = LabelType[label_type_str.upper()]
        except Exception as exc:
            logging.warning(f'encountered exception when detecting label type {exc}')
            label_type = None

        if label_type is None:
            logging.warning(f'could not determine valid label type for {name}')

        l = Label(name, label_type)
        l.color = _get_text_val(label, './color')

        for attr in label.findall('./attributes/attribute'):
            attr_name = _get_text_val(attr, './name')

            attr_type = None
            try:
                attr_type_str = _get_text_val(attr, './input_type')
                attr_type = InputType[attr_type_str.upper()]
            except:
                attr_type = None

            if attr_type is None:
                logging.warning(f'could not determine valid attribute input type for {name}')

            values = _get_text_val(attr, './values').split('\n')

            a = Attribute(attr_name, attr_type, values)

            a.mutable = _get_text_val(attr, './mutable') == 'True'
            a.default_value = _get_text_val(attr, './default_value')

            l.attributes[attr_name] = a

        d.labels[name] = l


def _parse_annotations(d: Dataset, root: Element):
    for image in root.findall('./image'):
        frame_name = image.attrib['name']
        frame_id = image.attrib.get('id', '0')
        frame_width = image.attrib.get('width', None)
        frame_height = image.attrib.get('height', None)

        if frame_width is not None:
            frame_width = int(frame_width)

        if frame_height is not None:
            frame_height = int(frame_height)

        frame = Frame(frame_name, frame_id, frame_width, frame_height)

        # loop over all annotations
        for child in image:
            label = child.attrib['label']
            rotation = 0

            z_order = 0
            if child.attrib.get('z_order', None) is not None:
                z_order = int(child.attrib['z_order'])

            occluded = False
            if child.attrib.get('occluded', None) is not None:
                occluded = child.attrib['occluded'] == '1'

            try:
                if child.tag == 'box':
                    xtl = float(child.attrib['xtl'])
                    ytl = float(child.attrib['ytl'])
                    xbr = float(child.attrib['xbr'])
                    ybr = float(child.attrib['ybr'])
                    geom = box(xtl, ybr, xbr, ytl)
                elif child.tag == 'polygon':
                    points = child.attrib['points'].split(';')
                    points = list(map(lambda x: list(map(lambda y: float(y), x.split(','))), points))
                    geom = Polygon(points)
                elif child.tag == 'polyline':
                    points = child.attrib['points'].split(';')
                    points = list(map(lambda x: list(map(lambda y: float(y), x.split(','))), points))
                    geom = LineString(points)
                elif child.tag == 'points':
                    points = child.attrib['points'].split(';')
                    points = list(map(lambda x: list(map(lambda y: float(y), x.split(','))), points))
                    if len(points) == 1:
                        geom = Point(points[0])
                    else:
                        geom = MultiPoint(points)
                elif child.tag == 'tag':
                    geom = Point(0,0)
                else:
                    logging.warning('unknown geometry type %s' % child.tag)
                    continue

                if child.attrib.get('rotation', None) is not None:
                    rotation = float(child.attrib['rotation'])
                    geom = shapely.affinity.rotate(geom, rotation)

                annotation = Annotation(frame, geom, label)
                annotation.rotation = rotation
                annotation.z_order = z_order
                annotation.occluded = occluded
                annotation.source = child.attrib.get('source', None)
                annotation.group = int(child.attrib.get('group_id', 0))

                # get attributes
                for attribute in child.findall('./attribute'):
                    annotation.attributes[attribute.attrib['name']] = attribute.text

                d.annotations.append(annotation)
            except Exception as exc:
                logging.warning(f'skipping annotation due to exception: {exc}')


def load(fh: Union[IO[str], str]) -> Dataset:
    '''
    Load a CVAT Images 1.1 XML file from `fh` as a dataset
    '''
    d = Dataset()

    tree = ET.parse(fh)
    root = tree.getroot()

    # parse xml sections
    _parse_meta(d, root)
    _parse_labels(d, root)
    _parse_annotations(d, root)

    return d


def loads(inp: str) -> Dataset:
    '''
    Load a CVAT Images 1.1 XML file from input string as a dataset
    '''
    return load(StringIO(inp))


def _dump_meta(obj: Dataset, root: Element):
    meta = ET.SubElement(root, 'meta')
    job = ET.SubElement(meta, 'job')

    ET.SubElement(job, 'id').text = obj.id
    ET.SubElement(job, 'size').text = str(len(obj.frames))

    if obj.mode is not None:
        ET.SubElement(job, 'mode').text = obj.mode

    ET.SubElement(job, 'overlap').text = str(obj.overlap)

    if obj.bugtracker is not None:
        ET.SubElement(job, 'bugtracker').text = obj.bugtracker

    if obj.created is not None:
        ET.SubElement(job, 'created').text = obj.created.isoformat()

    if obj.updated is not None:
        ET.SubElement(job, 'updated').text = obj.updated.isoformat()

    if obj.subset is not None:
        ET.SubElement(job, 'subset').text = obj.subset


def _dump_annotations(obj: Dataset, root: Element):
    for frame in obj.frames:
        frame_xml = ET.SubElement(root, 'image')
        frame_xml.attrib['id'] = frame.id
        frame_xml.attrib['name'] = frame.name

        if frame.width is not None:
            frame_xml.attrib['width'] = str(frame.width)

        if frame.height is not None:
            frame_xml.attrib['height'] = str(frame.height)

        for annotation in frame.annotations:
            label = obj.labels[annotation.label]
            annotation_xml: Element = None
            if label.type == LabelType.BBOX:
                annotation_xml = ET.SubElement(frame_xml, 'box')
                geom = copy(annotation.geom)

                # un-rotate if needed
                if annotation.rotation != 0:
                    geom = shapely.affinity.rotate(geom, -1 * annotation.rotation)

                coords_x, coords_y = geom.exterior.coords.xy
                annotation_xml.attrib['xtl'] = f'{coords_x[2]:.2f}'
                annotation_xml.attrib['ytl'] = f'{coords_y[1]:.2f}'
                annotation_xml.attrib['xbr'] = f'{coords_x[0]:.2f}'
                annotation_xml.attrib['ybr'] = f'{coords_y[0]:.2f}'
            elif label.type == LabelType.POLYGON:
                annotation_xml = ET.SubElement(frame_xml, 'polygon')
                geom = copy(annotation.geom)

                # un-rotate if needed
                if annotation.rotation != 0:
                    geom = shapely.affinity.rotate(geom, -1 * annotation.rotation)

                coords = list(geom.exterior.coords)
                annotation_xml.attrib['points'] = ';'.join(list(map(lambda x: f'{x[0]:.2f},{x[1]:.2f}', coords)))
            elif label.type == LabelType.POLYLINE:
                annotation_xml = ET.SubElement(frame_xml, 'polyline')
                coords = list(annotation.geom.coords)
                annotation_xml.attrib['points'] = ';'.join(list(map(lambda x: f'{x[0]:.2f},{x[1]:.2f}', coords)))
            elif label.type == LabelType.POINTS:
                annotation_xml = ET.SubElement(frame_xml, 'points')
                if annotation.geom.geom_type == 'MultiPoint':
                    points = []
                    for point in annotation.geom:
                        x = list(point.coords)
                        points.append(f'{x[0]:.2f},{x[1]:.2f}')
                    annotation_xml.attrib['points'] = ';'.join(points)
                else:
                    annotation_xml.attrib['points'] = list(map(lambda x: f'{x[0]:.2f},{x[1]:.2f}', coords))[0]
            elif label.type == LabelType.TAG:
                annotation_xml = ET.SubElement(frame_xml, 'tag')

            annotation_xml.attrib['label'] = annotation.label
            annotation_xml.attrib['id'] = annotation.id
            annotation_xml.attrib['occluded'] = '1' if annotation.occluded else '0'
            annotation_xml.attrib['z_order'] = str(annotation.z_order)

            if annotation.rotation != 0:
                annotation_xml.attrib['rotation'] = f'{annotation.rotation:.2f}'

            if annotation.group != 0:
                annotation_xml.attrib['group_id'] = str(annotation.group)

            if annotation.created_by is not None:
                annotation_xml.attrib['created_by'] = annotation.created_by

            if annotation.created_on is not None:
                annotation_xml.attrib['created_on'] = annotation.created_on.isoformat()

            for k, v in annotation.attributes.items():
                attr = ET.SubElement(annotation_xml, 'attribute')
                attr.attrib['name'] = k
                attr.text = v


def dump(obj: Dataset, fh: IO[str]):
    '''
    Save the dataset as a CVAT Images 1.1 XML file
    '''
    root = ET.Element('annotations')
    version = ET.SubElement(root, 'version')
    version.text = '1.1'

    _dump_meta(obj, root)
    _dump_annotations(obj, root)

    fh.write('<?xml version="1.0" encoding="utf-8"?>\n')
    ET.indent(root)
    fh.write(ET.dump(root))


def dumps(obj: Dataset) -> str:
    '''
    Dump the dataset to a string
    '''
    fh = StringIO()
    dump(obj, fh)
    fh.seek(0)
    return fh.read()
