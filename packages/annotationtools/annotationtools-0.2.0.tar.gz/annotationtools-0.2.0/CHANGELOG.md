# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2023-12-04

### Fixed

- Alias BBOX label type to RECTANGLE which some versions of CVAT use
- Fix bugs when reading and writing various CVAT files

### Changed

- Indexing `Datasets` now works like a list and returns the annotation at the associated index

## [0.1.0] - 2023-12-04

### Added

- Read and write of CVAT Images 1.1 XML format

[unreleased]: https://github.com/go-geospatial/annotation-tools/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/olivierlacan/keep-a-changelog/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/olivierlacan/keep-a-changelog/releases/tag/v0.1.0