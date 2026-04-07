from __future__ import annotations

import logging as logger
import os
import subprocess
import sys
from collections.abc import Generator
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import final, override

from cx_Freeze import Executable, setup
from setuptools import Command

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
_PACKAGE_NAME = "app"

try:
    __version__ = version(_PACKAGE_NAME)
except PackageNotFoundError:
    logger.warning(
        "Not found package name=%s, use default version=0.1.0", _PACKAGE_NAME
    )
    __version__ = "0.1.0"

build_exe_options: dict[str, object] = {
    "include_msvcr": True,
    "bin_excludes": ["api-ms-win-*.dll", "ucrtbase.dll"],
    "packages": [_PACKAGE_NAME],
    "excludes": ["*.log"],
    "includes": [
        "PySide6",
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
    ],
    "include_files": [],
}

bdist_msi_options = {
    # NOTE: Generate new UUID for this if necessary
    "upgrade_code": "{9e544e4c-1d1d-42b4-8ccd-3db6f226bf56}",
    # Per-user install (False -> per-machine)
    "all_users": False,
    # Do not modify PATH
    "add_to_path": False,
    # Default install directory
    "initial_target_dir": r"[LocalAppDataFolder]\Personal\App",
    # MSI filename base (without extension)
    "output_name": "App",
    # Lauch on finished
    "launch_on_finish": True,
    # Installer icon (optional)
    # "install_icon": "resources/icon.ico"
}

_base = "Win32GUI" if sys.platform == "win32" else "gui"
_target_name = "app.exe" if sys.platform == "win32" else "app"

executables = [
    Executable(
        script="src/app/__main__.py",
        base=_base,
        target_name=_target_name,
        # icon="Logo",
    )
]


def _walk_through(
    root: Path, ext: str | list[str] | None = None, exclude_path: Path | None = None
) -> Generator[Path]:
    if isinstance(ext, str):
        ext = [ext]

    items = os.listdir(root)

    for item in items:
        item_path = root / item
        if exclude_path is not None and item_path == exclude_path:
            continue
        if item_path.is_dir():
            yield from _walk_through(item_path, ext)
        else:
            _, item_ext = os.path.splitext(item)
            if ext is None or item_ext in ext:
                yield item_path


def build_all_qt_deps():
    build_ui()
    build_i18n()
    build_resources()


def build_resources():
    logger.info("Building resources...")
    resource_root = Path("resources").resolve()
    target_root = Path("src").resolve() / "app"

    for src in _walk_through(resource_root, ".qrc"):
        logger.info("Compiling resource: %s", src)
        rel = src.relative_to(resource_root)
        dst = (target_root / rel).with_suffix(".py")
        dst.parent.mkdir(parents=True, exist_ok=True)

        _ = subprocess.run(
            ["pyside6-rcc", src, "-o", str(dst).replace(".py", "_rc.py")], check=True
        )


def build_ui():
    logger.info("Building ui...")
    resource_root = Path("ui").resolve()
    target_root = Path("src").resolve() / "app" / "ui"

    # Clean old ui first
    if target_root.exists():
        import shutil

        shutil.rmtree(target_root)

    target_root.mkdir(parents=True, exist_ok=True)

    for src in _walk_through(resource_root, ".ui"):
        logger.info("Compiling resource: %s", src)
        rel = src.relative_to(resource_root)
        dst = (target_root / rel).with_suffix(".py")
        dst.parent.mkdir(parents=True, exist_ok=True)

        _ = subprocess.run(["pyside6-uic", "--from-imports", src, dst], check=True)
        # Fix the resource path
        text = dst.read_text()
        text = text.replace("from . import resources_rc", "from .. import resources_rc")
        _ = dst.write_text(text)


def build_i18n():
    print("Building i18n ...")
    # Need to scan both the raw .ui file and app .py file (exclude the ui files)
    i18n_root = Path("resources").resolve() / "i18n"
    i18n_root.mkdir(parents=True, exist_ok=True)
    ui_root = Path("ui").resolve()

    target_languages = list(_walk_through(i18n_root, ".ts"))
    # NOTE: Can add other paths to this list to create new translation

    target_files = list(_walk_through(ui_root, ext=".ui"))
    target_files.extend(
        list(_walk_through(Path("src"), ".py", exclude_path=Path("src") / "app" / "ui"))
    )

    # Update .ts files first
    for target_ts in target_languages:
        _ = subprocess.run(
            ["pyside6-lupdate", *target_files, "-ts", str(target_ts)], check=True
        )

    # Compile .ts file to .qm for translator
    for src in _walk_through(i18n_root, ".ts"):
        logger.info("Compiling resource: %s", src)
        dst = src.with_suffix(".qm")
        _ = subprocess.run(["pyside6-lrelease", src, "-qm", dst], check=True)


@final
class BuildQtDependencies(Command):
    descriptions = "Build all Qt dependency files: translator, resource, ui"
    user_options = []

    @override
    def initialize_options(self) -> None:
        pass

    @override
    def finalize_options(self) -> None:
        pass

    @override
    def run(self) -> None:
        build_all_qt_deps()


@final
class BuildResouces(Command):
    descriptions = "Build resource files"
    user_options = []

    @override
    def initialize_options(self) -> None:
        pass

    @override
    def finalize_options(self) -> None:
        pass

    @override
    def run(self) -> None:
        build_resources()


@final
class BuildUI(Command):
    descriptions = "Build ui files"
    user_options = []

    @override
    def initialize_options(self) -> None:
        pass

    @override
    def finalize_options(self) -> None:
        pass

    @override
    def run(self) -> None:
        build_ui()


@final
class BuildI18n(Command):
    descriptions = "Build i18n language only files"
    user_options = []

    @override
    def initialize_options(self) -> None:
        pass

    @override
    def finalize_options(self) -> None:
        pass

    @override
    def run(self) -> None:
        build_i18n()


args: dict[str, object] = {
    "data_files": [],
    "package_dir": {"": "src"},
    "packages": ["app"],
    "cmdclass": {
        "build_qt": BuildQtDependencies,
        "build_resources": BuildResouces,
        "build_i18n": BuildI18n,
        "build_ui": BuildUI,
    },
    "options": {
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    "executables": executables,
}


_ = setup(
    **args,
)
