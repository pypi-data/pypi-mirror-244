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

'''
Container class definitions for annotation-tools library
'''

from datetime import datetime
from uuid import uuid4
from typing import Dict, List
from enum import Enum

import pandas as pd
from shapely.geometry.base import BaseGeometry

class InputType(Enum):
    '''
    Indicator of type of control to use in user-interface for attributes
    '''
    SELECT = 1
    CHECKBOX = 2
    RADIO = 3
    NUMBER = 4
    TEXT = 5



class LabelType(Enum):
    '''
    Enumerate the geometry types that a label can have
    '''
    BBOX = 1
    POLYGON = 2
    POLYLINE = 3
    POINTS = 4
    TAG = 5
    RECTANGLE = 6



class Attribute:
    '''
    Attributes are additional information that can be stored on a label. Each attribute must
    have a name, input_type, and list of possible values
    '''

    def __init__(self, name: str, input_type: InputType, values: List[str]):
        self.name: str = name
        self.input_type: InputType = input_type
        self.mutable: bool = True
        self.default_value: str = None
        self.values: List[str] = values



class Label:
    '''
    Labels represent the canonical name used to identify an object within an image
    '''

    def __init__(self, name: str, label_type: LabelType, attributes: Dict[str, Attribute] = None):
        '''
        Create a new `Label` object

        Arguments:
            name: The label value, e.g. `car` or `tree`
            type: How the region of the image receiving said label is identified, e.g. BBOX
            attributes: Additional properties that can be applied to the label, e.g. vetted/un-vetted
        '''
        self.name: str = name
        self.type: str = label_type

        if attributes is None:
            self.attributes: Dict[str, Attribute] = {}
        else:
            self.attributes: Dict[str, Attribute] = attributes

        self.color: str = None
        self.parent: str = None


    def __getitem__(self, key) -> Attribute:
        return self.attributes[key]



class User:
    '''
    User objects uniquely identify an individual actor in the system
    '''

    def __init__(self, username: str, email: str = None):
        '''
        Create a new `User` object

        Arguments:
            username: Unique string that identifies the user
            email: Optional email address for the user
        '''
        self.username: str = username
        self.email: str = email



class Frame:
    '''
    Frames are individual images in the dataset and contain annotations
    '''

    def __init__(self, name: str, idx: str, width: int = None, height: int = None):
        self.name: str = name
        self.idx: str = idx
        self.width: int = width
        self.height: int = height
        self.annotations: set[Annotation] = set()



class Annotation:
    '''
    Annotations associate labels with specific regions on a frame (image).
    '''

    def __init__(self, frame: Frame, geom: BaseGeometry, label: str, annotation_id: str = None):
        '''
        Arguments:
            frame: path to the video or image
            id: index in lexical order of images
        '''
        self.frame: Frame = frame

        self.__id: str = annotation_id
        if self.__id is None:
            self.__id = str(uuid4())

        self.frame.annotations.add(self)

        self.geom: BaseGeometry = geom
        self.rotation: float = 0
        self.group: int = 0
        self.z_order: int = 0
        self.occluded: bool = False
        self.label: str = label
        self.source: str = 'manual'
        self.attributes: Dict[str, str] = {}

        self.created_by: str = None
        self.created_on: datetime = datetime.now()


    def __eq__(self, other):
        return self.id == other.id


    def __hash__(self):
        return hash(self.id)


    def __repr__(self):
        return f'{self.label} {self.geom}'


    def __getitem__(self, key):
        return self.attributes[key]


    def __getattr__(self, name):
        return self.attributes[name]


    @property
    def id(self):
        '''
        A unique identifier representing this annotation
        '''
        return self.__id



class Dataset:
    '''
    The Dataset class is a container that combines annotations with metadata.
    Metadata is stored directly as attributes on the dataset while the annotations themselves
    are stored in the `annotations` attribute.
    '''

    def __init__(self, annotations: List[Annotation] = None):
        self.id: str = str(uuid4())
        self.name: str = None
        self.size: int = None
        self.mode: str = None
        self.overlap: int = None
        self.bugtracker: str = None
        self.created: datetime = datetime.now()
        self.updated: datetime = None
        self.labels: Dict[str, Label] = {}
        self.owner: User = None
        self.subset: str = None

        if annotations is None:
            self.annotations: List[Annotation] = []
        else:
            self.annotations: List[Annotation] = annotations


    def __repr__(self):
        return f'<Dataset: {self.name} ({len(self.annotations)} annotations)>'


    def __len__(self):
        return len(self.annotations)


    def __getitem__(self, key) -> List[Annotation]:
        return self.annotations[key]


    def __iter__(self):
        return iter(self.annotations)


    def __contains__(self, key) -> bool:
        for annotation in self.annotations:
            if annotation.frame == key:
                return True

        return False


    @property
    def frames(self) -> List[Frame]:
        '''
        Get a list of frames associated with this dataset
        '''
        frames = set()
        for annotation in self.annotations:
            frames.add(annotation.frame)
        return list(frames)


    @property
    def dataframe(self):
        '''
        Get annotations as a pandas dataframe
        '''
        data = []
        for annotation in self:
            my_annotation = {
                'dataset_name': self.name,
                'frame': annotation.frame.name,
                'frame_idx': annotation.frame.id,
                'frame_height': annotation.frame.height,
                'frame_width': annotation.frame.width,
                'label': annotation.label,
                'geom': annotation.geom.wkt,
                'rotation': annotation.rotation,
                'occluded': annotation.occluded,
                'z_order': annotation.z_order,
                'annotation_id': annotation.id,
                'source': annotation.source,
                'group': annotation.group,
                'created_on': annotation.created_on,
                'created_by': annotation.created_by,
            }

            # add attributes
            my_annotation.update(annotation.attributes)

            data.append(my_annotation)

        return pd.DataFrame(data)
