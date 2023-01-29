from PyQt5.QtWidgets import QMainWindow, QListWidgetItem
from PyQt5 import QtCore
from ui_consult_window import Ui_ConsultWindow

from processor import Processor


class ConsultWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ConsultWindow, self).__init__(parent)
        self.ui = Ui_ConsultWindow()
        self.ui.setupUi(self)
        self.ui.butonUnselcetAll.clicked.connect(self.unselect_all)
        self.ui.listWidgetFacts.itemPressed.connect(self.toggle_item)
        self.ui.buttonProcess.clicked.connect(self.process_facts)

    def refresh_facts_list(self):
        database = self.parent().database
        self.ui.listWidgetFacts.clear()
        facts = []
        # for rule in database.get_rules():
        #     for fact in database.get_rule_conditions(rule):
        #         if fact not in facts:
        #             facts.append(fact)
        for rule in database.get_rules():
            facts += list(database.get_rule_conditions(rule))
        facts = database.sort_facts_by_name(list(set(facts)))
        for fact in facts:
            fact_item = QListWidgetItem(database.get_fact_name(fact))
            fact_item.item = fact
            fact_item.setFlags(fact_item.flags() | QtCore.Qt.ItemIsUserCheckable)
            fact_item.setCheckState(QtCore.Qt.Unchecked)
            self.ui.listWidgetFacts.addItem(fact_item)

    def toggle_item(self):
        item = self.ui.listWidgetFacts.currentItem()
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)

    def unselect_all(self):
        for i in range(self.ui.listWidgetFacts.count()):
            item = self.ui.listWidgetFacts.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                item.setCheckState(QtCore.Qt.Unchecked)

    def process_facts(self):
        database = self.parent().database
        facts = []
        for i in range(self.ui.listWidgetFacts.count()):
            fact_item = self.ui.listWidgetFacts.item(i)
            if fact_item.checkState() == QtCore.Qt.Checked:
                facts.append(fact_item.item)
        if facts:
            processor = Processor(facts, database)
            history = processor.process()
            self.ui.plainText.setPlainText(history)

    def showEvent(self, event) -> None:
        self.refresh_facts_list()
        super(ConsultWindow, self).showEvent(event)

    def closeEvent(self, event) -> None:
        self.parent().show()
        super(ConsultWindow, self).closeEvent(event)
