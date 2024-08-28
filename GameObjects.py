import Exceptions


class SpecialCondition:
    def __init__(self, name: str, function):  # функция должна иметь аргументы f(player_id, all_players, randomizer)
        self.name = name
        self.type = 'special_condition'
        self.function = function
        self.is_used = False

    def run(self, player, all_players, randomizer):
        if not self.is_used:
            self.function(player, all_players, randomizer)
            self.is_used = True
        else:
            raise Exceptions.SpecialConditionIsAlreadyUsed


class Occupation:
    def __init__(self, name: str, is_activated=False):
        self.name = name
        self.type = 'occupation'
        self.is_open = is_activated


class Biology:
    def __init__(self, name: str, is_activated=False):
        self.name = name
        self.is_open = is_activated
        self.type = 'biology'


class Character:
    def __init__(self, name: str, is_activated=False):
        self.name = name
        self.is_open = is_activated
        self.type = 'character'


class Health:
    def __init__(self, name: str, is_activated=False):
        self.name = name
        self.is_open = is_activated
        self.type = 'health'


class Hobby:
    def __init__(self, name: str, is_activated=False):
        self.name = name
        self.is_open = is_activated
        self.type = 'hobby'


class Phobia:
    def __init__(self, name: str, is_activated=False):
        self.name = name
        self.is_open = is_activated
        self.type = 'phobia'


class Inventory:
    def __init__(self, name: str, is_activated=False):
        self.name = name
        self.is_open = is_activated
        self.type = 'inventory'


class Fact:
    def __init__(self, name: str, is_activated=False):
        self.name = name
        self.is_open = is_activated
        self.type = 'fact'


class Player:
    def __init__(self, player_id: int, player_name: str, special_condition=SpecialCondition('', print), occupation='',
                 biology='', character='', health='', hobby='', phobia='', inventory='', fact='', votes=0):
        self.player_id = player_id
        self.player_name = player_name
        self.occupation = Occupation(occupation)
        self.biology = Biology(biology)
        self.character = Character(character)
        self.health = Health(health)
        self.hobby = Hobby(hobby)
        self.phobia = Phobia(phobia)
        self.inventory = Inventory(inventory)
        self.fact = Fact(fact)
        self.special_condition = special_condition
        self.votes = votes
        self.voted = False

    def reset_votes(self):
        self.votes = 0

    def update_player_id(self, new_player_id):
        self.player_id = new_player_id

    def update_player_name(self, new_player_name):
        self.player_name = new_player_name

    def update_occupation(self, new_occupation):
        self.occupation = new_occupation

    def update_biology(self, new_biology):
        self.biology = new_biology

    def update_character(self, new_character):
        self.character = new_character

    def update_health(self, new_health):
        self.health = new_health

    def update_hobby(self, new_hobby):
        self.hobby = new_hobby

    def update_phobia(self, new_phobia):
        self.phobia = new_phobia

    def update_inventory(self, new_inventory):
        self.inventory = new_inventory

    def update_fact(self, new_fact):
        self.fact = new_fact

    def update_special_condition(self, new_special_condition):
        self.special_condition = new_special_condition

    def get_shadow_cards_list(self):
        ans = []
        if not self.occupation.is_open:
            ans.append(self.occupation)
        if not self.biology.is_open:
            ans.append(self.biology)
        if not self.character.is_open:
            ans.append(self.character)
        if not self.health.is_open:
            ans.append(self.health)
        if not self.hobby.is_open:
            ans.append(self.hobby)
        if not self.phobia.is_open:
            ans.append(self.phobia)
        if not self.inventory.is_open:
            ans.append(self.inventory)
        if not self.fact.is_open:
            ans.append(self.fact)
        return ans

    def get_open_cards_list(self):
        ans = []
        if self.occupation.is_open:
            ans.append(self.occupation)
        if self.biology.is_open:
            ans.append(self.biology)
        if self.character.is_open:
            ans.append(self.character)
        if self.health.is_open:
            ans.append(self.health)
        if self.hobby.is_open:
            ans.append(self.hobby)
        if self.phobia.is_open:
            ans.append(self.phobia)
        if self.inventory.is_open:
            ans.append(self.inventory)
        if self.fact.is_open:
            ans.append(self.fact)
        return ans

    def open_card(self, card_type: str):
        if card_type == 'occupation':
            self.occupation.is_open = True
        elif card_type == 'biology':
            self.biology.is_open = True
        elif card_type == 'character':
            self.character.is_open = True
        elif card_type == 'health':
            self.health.is_open = True
        elif card_type == 'hobby':
            self.hobby.is_open = True
        elif card_type == 'phobia':
            self.phobia.is_open = True
        elif card_type == 'inventory':
            self.inventory.is_open = True
        elif card_type == 'fact':
            self.fact.is_open = True
        else:
            pass

    def get_open_cards_count(self):
        return len(self.get_open_cards_list())


class Catastrophe:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

