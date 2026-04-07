from __future__ import annotations

import signal
import sys
from typing import Never, final

from PySide6 import QtCore, QtGui, QtWidgets

from app import resources_rc  # noqa: F401  # pyright: ignore[reportUnusedImport]
from app.const.app import APP_DISPLAY_NAME, APP_NAME, APP_ORG_NAME
from app.utils.logging import get_logger, setup_logger
from app.widgets.main_window import MainWindow

logger = get_logger()


@final
class MyApp(QtWidgets.QApplication):
    def __init__(self) -> None:
        super().__init__(sys.argv)

        self.setApplicationName(APP_NAME)
        self.setOrganizationName(APP_ORG_NAME)
        self.setDesktopFileName(APP_DISPLAY_NAME)

        self._setting = QtCore.QSettings()

        self._default_language = "en"
        self.window: MainWindow = MainWindow(APP_DISPLAY_NAME, self._default_language)

        self._translator: QtCore.QTranslator | None = None

        _ = self.window.language_change_signal.connect(self.change_language_to)

    def change_language_to(self, language: str) -> None:
        if self._translator is not None:
            _ = self.removeTranslator(self._translator)
            self._translator = None

        if language == self._default_language:
            return

        translator: QtCore.QTranslator = QtCore.QTranslator(self)
        qm_path = f":/translator/i18n/{language}.qm"

        if not translator.load(qm_path):
            return

        _ = self.installTranslator(translator)
        self._translator = translator


def lauch() -> Never:
    setup_logger()  # NOTE: Could parse args here
    QtGui.QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    QtGui.qt_set_sequence_auto_mnemonic(True)

    _ = signal.signal(signalnum=signal.SIGINT, handler=signal.SIG_DFL)

    app: MyApp = MyApp()
    sys.exit(app.exec())


if __name__ == "__main__":
    lauch()
