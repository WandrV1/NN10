from PyQt5.QtWidgets import QMainWindow, QInputDialog, QListWidgetItem
from ui_database_edit_window import Ui_DatabaseEditWindow
from common_ui import message_error, message_info


class DatabaseEditWindow(QMainWindow):
    def __init__(self, parent=None):
        super(DatabaseEditWindow, self).__init__(parent)
        self.ui = Ui_DatabaseEditWindow()
        self.ui.setupUi(self)
        self.ui.buttonFactsAdd.clicked.connect(self.create_fact)
        self.ui.buttonFactsRename.clicked.connect(self.rename_fact)
        self.ui.buttonFactsDelete.clicked.connect(self.delete_fact)
        self.ui.buttonRulesAdd.clicked.connect(self.create_rule)
        self.ui.buttonRulesDelete.clicked.connect(self.delete_rule)
        self.ui.listWidgetRules.currentItemChanged.connect(self.refresh_rule_conditions)
        self.ui.buttonRulesFactsAdd.clicked.connect(self.add_rule_condition)
        self.ui.buttonRulesFactsDelete.clicked.connect(self.remove_rule_condition)

    def create_fact(self):
        database = self.parent().database
        fact_name, ok = QInputDialog.getText(self, 'Создание факта', 'Введите название факта:')
        if ok and fact_name:
            if database.create_fact(fact_name) == 1:
                self.refresh_facts_list()
            else:
                message_error(self, 'Ошибка при создании факта')

    def delete_fact(self):
        database = self.parent().database
        fact_item = self.ui.listWidgetFacts.currentItem()
        if fact_item is not None:
            if database.delete_fact(fact_item.item) == 1:
                self.refresh_facts_list()
                self.refresh_rules_list()
            else:
                message_error(self, 'Ошибка при удалении факта')
            self.ui.listWidgetFacts.setCurrentItem(None)

    def rename_fact(self):
        database = self.parent().database
        fact_item = self.ui.listWidgetFacts.currentItem()
        if fact_item is not None:
            fact_name, ok = QInputDialog.getText(self, 'Изменение факта',
                                                 'Введите название факта:', text=database.get_fact_name(fact_item.item))
            if ok and fact_name:
                if database.set_fact_name(fact_item.item, fact_name) != -1:
                    self.refresh_facts_list()
                    self.refresh_rules_list()
                else:
                    message_error(self, 'Ошибка при редактировании факта')
            self.ui.listWidgetFacts.setCurrentItem(None)

    def refresh_facts_list(self):
        database = self.parent().database
        self.ui.listWidgetFacts.clear()
        facts = database.sort_facts_by_name(database.get_facts())
        for fact in facts:
            fact_item = QListWidgetItem(database.get_fact_name(fact))
            fact_item.item = fact
            self.ui.listWidgetFacts.addItem(fact_item)

    def refresh_rules_list(self):
        database = self.parent().database
        self.ui.listWidgetRules.clear()
        rules = database.sort_rules_by_name(database.get_rules())
        for rule in rules:
            # rule_item = QListWidgetItem(database.get_rule_name(rule))
            rule_item = QListWidgetItem(database.get_rule_full_name(rule))
            rule_item.item = rule
            self.ui.listWidgetRules.addItem(rule_item)

    def refresh_rule_conditions(self):
        database = self.parent().database
        self.ui.listWidgetRulesFacts.clear()
        rule_item = self.ui.listWidgetRules.currentItem()
        if rule_item is not None:
            rule_conditions = database.sort_facts_by_name(database.get_rule_conditions(rule_item.item))
            for condition in rule_conditions:
                condition_item = QListWidgetItem(database.get_fact_name(condition))
                condition_item.item = condition
                self.ui.listWidgetRulesFacts.addItem(condition_item)

    def add_rule_condition(self):
        database = self.parent().database
        rule_item = self.ui.listWidgetRules.currentItem()
        if rule_item is not None:
            rule = rule_item.item
            reserved_facts = [database.get_rule_action(rule)]
            for condition in database.get_rule_conditions(rule):
                reserved_facts.append(condition)
            available_facts = [database.get_fact_name(fact) for fact in database.sort_facts_by_name(database.get_facts()) if fact not in reserved_facts]
            if not available_facts:
                message_info(self, 'Нет доступных фактов для добавления')
                return
            fact_name, ok = QInputDialog.getItem(self, 'Выбор антецедента', 'Выберите антецедент правила:', available_facts, 0, False)
            if ok:
                fact = database.get_fact_by_name(fact_name)
                if database.set_rule_condition(rule, fact) == 0:
                    rule_item.setText(database.get_rule_full_name(rule))
                    self.refresh_rule_conditions()
                else:
                    message_error(self, 'Ошибка при добавлении правила')

    def remove_rule_condition(self):
        database = self.parent().database
        rule_item = self.ui.listWidgetRules.currentItem()
        if rule_item is not None:
            rule = rule_item.item
            fact_item = self.ui.listWidgetRulesFacts.currentItem()
            if fact_item is not None:
                if database.remove_rule_condition(rule, fact_item.item) == 0:
                    rule_item.setText(database.get_rule_full_name(rule))
                    self.refresh_rule_conditions()
                else:
                    message_error(self, 'Ошибка при удалении факта из правила')
                self.ui.listWidgetRulesFacts.setCurrentItem(None)

    def create_rule(self):
        database = self.parent().database
        if fact_names := [database.get_fact_name(fact) for fact in database.sort_facts_by_name(database.get_facts())]:
            action_name, ok = QInputDialog.getItem(self, 'Выбор консеквента',
                                                   'Выберите консеквент правила:', fact_names, 0, False)
            if ok:
                action = database.get_fact_by_name(action_name)
                if database.create_rule(action) == 1:
                    self.refresh_rules_list()
                else:
                    message_error(self, 'Ошибка при создании правила')
        else:
            message_info(self, "Невозможно создать правила\nесли в базе знаний нет фактов")

    def delete_rule(self):
        database = self.parent().database
        rule_item = self.ui.listWidgetRules.currentItem()
        if rule_item is not None:
            if database.delete_rule(rule_item.item) == 1:
                self.refresh_rules_list()
            else:
                message_error(self, 'Ошибка при удалении правила')
            self.ui.listWidgetFacts.setCurrentItem(None)

    def showEvent(self, event) -> None:
        self.refresh_facts_list()
        self.refresh_rules_list()
        super(DatabaseEditWindow, self).showEvent(event)

    def closeEvent(self, event) -> None:
        self.parent().show()
        super(DatabaseEditWindow, self).closeEvent(event)
