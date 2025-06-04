# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# [0.1.x]

## [0.1.5] - 2025-06-04

### Fixed

- Imports to ``spark3dbatch`` module.

## [0.1.4] - 2025-06-04

### Fixed

- Added a `__init__.py` to allow imports.

## [0.1.3] - 2025-06-04

### Changed

- Project name is now `spark3d-batch`.

## [0.1.2] - 2025-06-04

### Added

- Workflow to release on PyPI.

## [0.1.1] - 2025-06-04

### Added

- Function converting accelerating field to power.

### Changed

- The code now requires the environment variable `$SPARK3DPATH` to be set, and to point to where the `spark3d` binary is located.

## [0.1.0] - 2025-06-04

### Added

- A `pyproject.toml`, so that package can be installed with `pip install -e .`
- `pre-commit`

### Changed

- Code structure, with source in `src/spark3dbatch`.
- Packaged data.
- Type hints, PEP8 conventions.


<!-- ## [0.0.0] 1312-01-01 -->
<!---->
<!-- ### Added -->
<!---->
<!-- ### Changed -->
<!---->
<!-- ### Deprecated -->
<!---->
<!-- ### Removed -->
<!---->
<!-- ### Fixed -->
<!---->
<!-- ### Security -->
