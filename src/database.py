from peewee import SqliteDatabase, Model, AutoField, CharField, ManyToManyField, ForeignKeyField, IntegrityError

db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class Fact(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(unique=True)

    def __str__(self):
        return self.name


class Rule(BaseModel):
    id = AutoField(primary_key=True)
    action = ForeignKeyField(Fact, on_delete='CASCADE')
    conditions = ManyToManyField(Fact, backref='rules', on_delete='CASCADE')

    def __str__(self):
        return f'П{self.id}: {self.action}'

    def get_full_name(self):
        return f'(П{self.id}) {str(self.conditions[0]) if len(self.conditions) > 0 else ""}' \
               f'{"".join(f"&{str(condition)}" for condition in self.conditions[1:])} -> {str(self.action)}'

    def get_short_name(self):
        return f'П{self.id}'


class Database:
    def __init__(self, database_path: str, init_mode: bool) -> None:
        db.init(database_path, pragmas={'journal_mode': 'wal', 'foreign_keys': 'on'})
        if init_mode:
            db.drop_tables([Fact, Rule, Rule.conditions.get_through_model()])
        db.create_tables([Fact, Rule, Rule.conditions.get_through_model()])

    def get_facts(self) -> list[Fact]:
        return Fact.select()

    def create_fact(self, fact_name: str) -> int:
        fact = Fact(name=fact_name)
        try:
            return fact.save()
        except IntegrityError:
            return -1

    def get_fact_name(self, fact: Fact) -> str:
        return fact.name

    def get_fact_by_name(self, name: str) -> str:
        return Fact.get(Fact.name == name)

    def set_fact_name(self, fact: Fact, name: str) -> int:
        fact.name = name
        try:
            return fact.save()
        except IntegrityError:
            return -1

    def delete_fact(self, fact: Fact) -> int:
        return fact.delete_instance()

    def get_rules(self) -> list[Rule]:
        return Rule.select()

    def create_rule(self, action: Fact) -> int:
        rule = Rule(action=action)
        try:
            return rule.save()
        except IntegrityError:
            return -1

    def get_rule_name(self, rule: Rule) -> str:
        return str(rule)

    def get_rule_full_name(self, rule: Rule) -> str:
        return rule.get_full_name()

    def get_rule_short_name(self, rule: Rule) -> str:
        return rule.get_short_name()

    def get_rule_action(self, rule: Rule) -> Fact:
        return rule.action

    def get_rule_conditions(self, rule: Rule) -> list[Fact]:
        return rule.conditions

    def set_rule_condition(self, rule: Rule, condition: Fact) -> int:
        try:
            rule.conditions.add(condition)
            return 0
        except IntegrityError:
            return -1

    def remove_rule_condition(self, rule: Rule, condition: Fact) -> int:
        try:
            rule.conditions.remove(condition)
            return 0
        except IntegrityError:
            return -1

    def delete_rule(self, rule: Rule) -> int:
        return rule.delete_instance()

    def sort_facts_by_name(self, facts: list[Fact]) -> list[Fact]:
        return sorted(facts, key=lambda x: x.name, reverse=False)

    def sort_rules_by_name(self, rules: list[Rule]) -> list[Rule]:
        return sorted(rules, key=lambda x: str(x), reverse=False)


if __name__ == '__main__':
    def is_subset(rule_facts, facts_slice):
        return False if len(rule_facts) == 0 else set(rule_facts).issubset(facts_slice)


    database = Database('testbase.db', True)
    # Сортировка элементов списка
    # database.create_fact("Ангина")
    # database.create_fact("Вода")
    # database.create_fact("Ярослав")
    # database.create_fact("Геннадий")
    # database.create_fact("Святослав")
    # sorted_facts = database.sort_facts_by_name(database.get_facts())
    # for fact in sorted_facts:
    #     print(fact)
    # database.create_rule(database.get_facts()[0])
    # database.create_rule(database.get_facts()[2])
    # database.create_rule(database.get_facts()[4])
    # sorted_rules = database.sort_rules_by_name(database.get_rules())
    # for rule in sorted_rules:
    #     print(rule)

    # Наблюдаем каскадное удаление
    # database.create_fact('fact1')
    # database.create_fact('fact2')
    # # database.create_fact('fact3')
    # database.create_rule(database.get_facts()[0])
    # database.set_rule_condition(database.get_rules()[0], database.get_facts()[1])
    # # database.set_rule_condition(database.get_rules()[0], database.get_facts()[2])
    # rules = database.get_rules()
    # for rule in rules:
    #     print(database.get_rule_full_name(rule))
    # database.delete_fact(database.get_facts()[0])
    # rules = database.get_rules()
    # for rule in rules:
    #     print(database.get_rule_full_name(rule))

    # Проверка функционала подмножеств
    # database.create_fact('fact1')
    # database.create_fact('fact2')
    # database.create_fact('fact3')
    # database.create_fact('fact4')
    # database.create_rule('somerule')
    # facts_slice = database.get_facts()[:3]
    # database.set_rule_fact(database.get_rules()[0], database.get_facts()[0])
    # rule_facts = database.get_rule_facts(database.get_rules()[0])
    # unique_facts = [fact for fact in facts_slice if fact not in rule_facts]
    # for fact in unique_facts:
    #     print(fact)
    # print(is_subset(rule_facts, facts_slice))

    # database.create_fact('somefact')
    #
    # database.create_rule('somerule')
    # database.create_rule('newrule')
    # rules = database.get_rules()
    # for rule in rules:
    #     print(rule)
    # my_rule = database.get_rules()[0]
    # my_fact = database.get_facts()[0]
    # database.set_rule_fact(my_rule, my_fact)
    # rule_facts = database.get_rule_facts(my_rule)
    # for fact in rule_facts:
    #     print(fact)
    # database.delete_rule(my_rule)
    # # my_rule.delete_instance()
    #
    # facts = database.get_facts()
    # for fact in facts:
    #     print(fact)
    #
    # database.create_rule('somerule')
    # print(len(database.get_rules()))
    # rules = database.get_rules()
    # for rule in rules:
    #     print(rule)
