def is_subset(rule_facts, facts_slice):
    return False if len(rule_facts) == 0 else set(rule_facts).issubset(set(facts_slice))


from database import Fact, Rule, Database


class Processor:
    def __init__(self, facts: list[Fact], database: Database) -> None:
        self.memory: list[Fact] = facts
        self.start_memory: list[Fact] = self.memory.copy()
        self.database = database
        self.history = str()

    def process(self) -> str:
        step_counter = 1
        accomplished_rules = []
        while True:
            conf_set = []
            rules = self.database.get_rules()
            for rule in rules:
                if rule not in accomplished_rules and self.database.get_rule_action(rule) not in self.memory:
                    rule_conditions = self.database.get_rule_conditions(rule)
                    if self.is_subset(rule_conditions, self.memory):
                        conf_set.append(rule)
            if not conf_set:
                if self.history:
                    # result_memory = [fact for fact in self.memory if fact not in self.start_memory]
                    result_memory = self.database.sort_facts_by_name(list(set(self.memory) - set(self.start_memory)))
                    # memory_str = f'РП=[{"".join(f"{self.database.get_fact_name(fact)}; " for fact in self.database.sort_facts_by_name(self.memory))}]'
                    memory_str = f'РП=[{"".join(f"{self.database.get_fact_name(fact)}; " for fact in result_memory)}]'
                    result_memory = [fact for fact in self.memory if fact not in self.start_memory]
                    self.history = f'{self.history}Итог\n{memory_str}'
                elif len(self.memory) == len(self.database.get_facts()):
                    self.history = 'Нет необходимости проводить логический вывод'
                else:
                    self.history = 'Доступных для выполнения правил не найдено'
                return self.history
            chosen_rule = conf_set[0]

            # Запись истории
            memory_str = f'РП=[{"".join(f"{self.database.get_fact_name(fact)}; " for fact in self.memory)}]'
            conf_set_str = f'КН=[{"".join(f"{self.database.get_rule_short_name(rule)}; " for rule in conf_set)}]'
            chosen_rule_str = f'Выбранное правило: {self.database.get_rule_full_name(chosen_rule)}'
            self.history = f'{self.history}Шаг {step_counter}\n{memory_str}\n{conf_set_str}\n{chosen_rule_str}\n\n'
            self.memory.append(self.database.get_rule_action(chosen_rule))
            accomplished_rules.append(chosen_rule)
            step_counter += 1

    def is_subset(self, subset: list[Fact], base_set: list[Fact]) -> bool:
        return set(subset).issubset(set(base_set)) if subset else False
