from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

APP_NAME = "TemplateApp"
APP_ORG_NAME = "YourOrganization"  # Organization name is required for QSettings
APP_DISPLAY_NAME = "Qt Template App"

try:
    __version__ = version("app")
except PackageNotFoundError:
    __version__ = "0.1.0"

APP_VERSION_STR = str(__version__)
BUILD_VERSION_STR = str(__version__) + "b.0"  # Define logic if need
