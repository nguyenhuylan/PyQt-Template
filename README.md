# PySide6/PyQt6 GUI Template

## Introduction

A minimal, structured template for building and distributing Python Qt GUI applications.
Created based on Pyside6, but can switch to PyQt6 by changing package and build command inside `setup.py`

**Designed for**:

- Fast setup
- Clean build pipeline
- Simple deployment via cx_Freeze

**Features**:
* Qt GUI architecture
* Centralized build system via setup.py
* Qt asset pipeline:
  * UI (.ui → .py)
  * Resources (.qrc → compiled)
  * Internationalization (i18n)
* Single-command packaging into executable
* uv-based workflow for reproducibility

## Requirements

* Python 3.10+
* uv
* PySide6
* cx_Freeze

## Usage

### 1. Build Qt Components

Compile all Qt-related assets:

```bash
uv run setup.py build_qt
```

Or run individually:

```bash

# Resources (build resources.py from .qrc only)
uv run setup.py build_resources

# Translations (extract + compile to .qm)
uv run setup.py build_i18n

# UI files (.ui → .py)
uv run setup.py build_ui
```

### 2. Run Application

(Adjust based on your entry point)

```bash
uv run -m app
```

### 3. Build Application

Building using cx_Freeze:

```bash
uv run setup.py build
```

Or optional formats (follow cv_freeze docs):
```bash
# Windows installer
uv run setup.py bdis_msi

# Other formats supported by cx_Freeze
uv run setup.py <command>
```

## Project Structure (Example)

```bash
<root>
|-- resources/
|    |-- assets/
|    |-- i18n/
|    |-- resources.qrc
|-- src/app/
|    |-- __init__.py  
|    |-- __main__.py  
|-- ui/
|-- README.md
|-- pyproject.toml
|-- ruff.toml
|-- setup.py
```

## Customization

Modify setup.py to:

* Change entry point
* Add dependencies
* Tune build options (icons, includes, excludes)

## Notes

* Always rebuild Qt assets after modifying .ui, .qrc, or translations.

## Minimal Workflow

```bash
# Rebuild resource
uv run setup.py build_qt

# Run directly/test
uv run -m app

# build/deploy
uv run setup.py build
```
