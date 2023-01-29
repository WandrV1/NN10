import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from ui_main_window import Ui_MainWindow
from database_edit_window import DatabaseEditWindow
from consult_window import ConsultWindow
from database import Database


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.database = None
        self.database_edit_window = DatabaseEditWindow(self)
        self.consult_window = ConsultWindow(self)
        self.ui.buttonLoadDatabase.clicked.connect(self.database_open)
        self.ui.buttonInitEmptyDatabase.clicked.connect(self.database_init)
        self.ui.buttonBaseEditMode.clicked.connect(self.open_database_edit_window)
        self.ui.buttonConsultMode.clicked.connect(self.open_consult_window)

    def open_database_edit_window(self):
        self.hide()
        self.database_edit_window.show()

    def open_consult_window(self):
        self.hide()
        self.consult_window.show()

    def database_open(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Database open',
                                                  os.getcwd(), 'Database files (*.db)')
        if filename:
            self.database = Database(database_path=filename, init_mode=False)
            self.ui.buttonBaseEditMode.setEnabled(True)
            self.ui.buttonConsultMode.setEnabled(True)

    def database_init(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Database create',
                                                  f'{os.getcwd()}/database.db', 'Database files (*.db)')
        if filename:
            self.database = Database(database_path=filename, init_mode=True)
            self.ui.buttonBaseEditMode.setEnabled(True)
            self.ui.buttonConsultMode.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    exit(app.exec())
