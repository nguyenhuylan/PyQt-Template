from __future__ import annotations

from typing import final, override

from PySide6.QtCore import QEvent, QResource, Signal
from PySide6.QtWidgets import QMainWindow, QWidget

from app import resources_rc  # noqa: F401  # pyright: ignore[reportUnusedImport]
from app.ui.main_window import Ui_MainWindow
from app.ui.sample_widgets import Ui_Form


@final
class MainWindow(QMainWindow, Ui_MainWindow):
    language_change_signal: Signal = Signal(str)

    def __init__(self, base_title: str, default_language: str, *args, **kwargs):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        super().__init__(*args, **kwargs)  # pyright: ignore[reportUnknownArgumentType]
        self.setupUi(self)  # pyright: ignore[reportUnknownMemberType]

        self._base_title = base_title
        self._default_language = default_language

        self.form_widget = QWidget(self)
        self.form_ui = Ui_Form()
        self.form_ui.setupUi(self.form_widget)  # pyright: ignore[reportUnknownMemberType]
        self.form_ui.language_select_box.insertItems(0, self._get_available_language())
        self.setCentralWidget(self.form_widget)

        _ = self.form_ui.language_select_box.currentIndexChanged.connect(
            lambda: self.language_change_signal.emit(
                self.form_ui.language_select_box.currentText()
            )
        )
        self.show()

    def _get_available_language(self) -> list[str]:
        languages = [self._default_language]
        res = QResource(":/translator/i18n")
        if not res.isValid():
            return languages
        qm_files = res.children()
        for path in qm_files:
            languages.append(path.removesuffix(".qm"))

        return languages

    @override
    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslateUi(self)  # pyright: ignore[reportUnknownMemberType]
            self.form_ui.retranslateUi(  # pyright: ignore[reportUnknownMemberType]
                self.form_widget
            )  # This should be handler inside the widget if you create it separately
            self.setWindowTitle(self.tr(self._base_title))

        super().changeEvent(event)
