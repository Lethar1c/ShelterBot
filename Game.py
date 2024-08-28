from GameObjects import Catastrophe, Player
import Randomizer
import time
from aiogram.types import Message


class Game:
    def __init__(self, catastrophe: Catastrophe, player_list: [Player], randomizer: Randomizer.GameRandomizer,
                 game_id: int, group_id: int):
        self.group_id = group_id
        self.game_id = game_id
        self.timer = time.time()
        self.catastrophe = catastrophe
        self.player_list = player_list
        self.randomizer = randomizer
        self.step = 1
        self.is_active = False
        self.number_of_players = len(player_list)
        self.message: Message
        self.stay_in_shelter = self.number_of_players // 2 + self.number_of_players % 2
        self.max_step = 2 + len(player_list) - (len(player_list) // 2 + len(player_list) % 2)
        self.special_conditions_in_round = {}

    def add_player(self, player: Player):
        self.player_list.append(player)
        self.number_of_players += 1
        self.stay_in_shelter = self.number_of_players // 2 + self.number_of_players % 2

    def set_active(self):
        self.is_active = True

    def set_inactive(self):
        self.is_active = False

    def generate_cards(self):
        self.catastrophe = self.randomizer.generate_catastrophe()
        for player in self.player_list:
            player.update_occupation(self.randomizer.generate_occupation())
            player.update_hobby(self.randomizer.generate_hobby())
            player.update_biology(self.randomizer.generate_biology())
            player.update_character(self.randomizer.generate_character())
            player.update_fact(self.randomizer.generate_fact())
            player.update_health(self.randomizer.generate_health())
            player.update_inventory(self.randomizer.generate_inventory())
            player.update_phobia(self.randomizer.generate_phobia())
            player.update_special_condition(self.randomizer.generate_special_condition())

    def eliminate_player(self, player_id: int):
        i = 0
        for player in self.player_list:
            if player_id == player.player_id:
                self.player_list.pop(i)
                self.number_of_players -= 1
            i += 1

    def start_game(self):
        self.is_active = True

    def get_player_name_list(self):
        res = []
        for player in self.player_list:
            res.append(player.player_name)
        return res

    def get_player_id_list(self):
        res = []
        for player in self.player_list:
            res.append(player.player_id)
        return res

    def get_open_cards_list(self):
        ans = {}
        for player in self.player_list:
            ans[player] = []
            if player.occupation.is_open:
                ans[player].append(f"Профессия: **{player.occupation.name}**")
            if player.biology.is_open:
                ans[player].append(f"Биологические данные: **{player.biology.name}**")
            if player.character.is_open:
                ans[player].append(f"Характер: **{player.character.name}**")
            if player.health.is_open:
                ans[player].append(f"Здоровье: **{player.health.name}**")
            if player.hobby.is_open:
                ans[player].append(f"Хобби: **{player.hobby.name}**")
            if player.phobia.is_open:
                ans[player].append(f"Фобия: **{player.phobia.name}**")
            if player.inventory.is_open:
                ans[player].append(f"Багаж: **{player.inventory.name}**")
            if player.fact.is_open:
                ans[player].append(f"Факт: **{player.fact.name}**")
        return ans

