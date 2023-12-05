# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.2

### Changed

- Allow Django 5.0

### Removed

- Remove support for Django versions below 4.2
- Remove support for Python versions below 3.10

## 1.1.1

### Changed

- Allow Django 4.0

## 1.1

### Added
- Add changelog

### Changed
- Use poetry as packaging system and replace ``setup.py`` with ``pyproject.toml``.

### Removed
- Remove support for Django versions below 2.2.

## 1.0.3.post1

### Changed
- Relicence under Apache License 2.0.
- Move repository to AlekSIS group on edugit.org.

## 1.0.3.post0

### Fixed
- Add missing instructions in README.rst.

## 1.0.3

### Fixed
- Replace ``Context`` objects with plain dictionaries in template tag code.

## 1.0.2

### Fixed
- Include template tags in package distribution.
- Fix dictionary lookup in template tags.

## 1.0

### Added
- Add template tags to readably include JavaScript/CSS files in templates.
