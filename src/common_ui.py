from PyQt5.QtWidgets import QMessageBox


def message_critical(parent, message_text: str):
    QMessageBox.critical(parent, 'Critical error', message_text)


def message_error(parent, message_text: str):
    QMessageBox.warning(parent, 'Warning', message_text)


def message_info(parent, message_test: str):
    QMessageBox.information(parent, 'Info', message_test)
