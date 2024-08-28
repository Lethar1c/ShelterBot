import GameObjects
import random


def change_occupation(player: GameObjects.Player, all_players: list[GameObjects.Player], randomizer):
    player.update_occupation(randomizer.generate_occupation())


def change_biology(player: GameObjects.Player, all_players: list[GameObjects.Player], randomizer):
    player.update_biology(randomizer.generate_biology())


def change_character(player: GameObjects.Player, all_players: list[GameObjects.Player], randomizer):
    player.update_character(randomizer.generate_character())


def change_health(player: GameObjects.Player, all_players: list[GameObjects.Player], randomizer):
    player.update_health(randomizer.generate_health())


def change_hobby(player: GameObjects.Player, all_players: list[GameObjects.Player], randomizer):
    player.update_hobby(randomizer.generate_hobby())


def change_phobia(player: GameObjects.Player, all_players: list[GameObjects.Player], randomizer):
    player.update_phobia(randomizer.generate_phobia())


def change_inventory(player: GameObjects.Player, all_players: list[GameObjects.Player], randomizer):
    player.update_inventory(randomizer.generate_inventory())


def change_fact(player: GameObjects.Player, all_players: list[GameObjects.Player], randomizer):
    player.update_fact(randomizer.generate_fact())


def shuffle_occupation(player: GameObjects.Player, all_players: list[GameObjects.Player], randomizer):
    player_list = []
    occupation_list = []
    for player in all_players:
        if player.occupation.is_open:
            player_list.append(player)
            occupation_list.append(player.occupation)
    random.shuffle(occupation_list)
    for i in range(len(player_list)):
        player_list[i].update_occupation(occupation_list[i])


def shuffle_biology(player: GameObjects.Player, all_players: list[GameObjects.Player], randomizer):
    player_list = []
    biology_list = []
    for player in all_players:
        if player.biology.is_open:
            player_list.append(player)
            biology_list.append(player.biology)
    random.shuffle(biology_list)
    for i in range(len(player_list)):
        player_list[i].update_biology(biology_list[i])


def shuffle_character(player: GameObjects.Player, all_players: list[GameObjects.Player], randomizer):
    player_list = []
    character_list = []
    for player in all_players:
        if player.character.is_open:
            player_list.append(player)
            character_list.append(player.character)
    random.shuffle(character_list)
    for i in range(len(player_list)):
        player_list[i].update_character(character_list[i])


def shuffle_health(player: GameObjects.Player, all_players: list[GameObjects.Player], randomizer):
    player_list = []
    health_list = []
    for player in all_players:
        if player.health.is_open:
            player_list.append(player)
            health_list.append(player.health)
    random.shuffle(health_list)
    for i in range(len(player_list)):
        player_list[i].update_health(health_list[i])


def shuffle_hobby(player: GameObjects.Player, all_players: list[GameObjects.Player], randomizer):
    player_list = []
    hobby_list = []
    for player in all_players:
        if player.hobby.is_open:
            player_list.append(player)
            hobby_list.append(player.hobby)
    random.shuffle(hobby_list)
    for i in range(len(player_list)):
        player_list[i].update_hobby(hobby_list[i])


def shuffle_phobia(player: GameObjects.Player, all_players: list[GameObjects.Player], randomizer):
    player_list = []
    phobia_list = []
    for player in all_players:
        if player.phobia.is_open:
            player_list.append(player)
            phobia_list.append(player.phobia)
    random.shuffle(phobia_list)
    for i in range(len(player_list)):
        player_list[i].update_phobia(phobia_list[i])


def shuffle_inventory(player: GameObjects.Player, all_players: list[GameObjects.Player], randomizer):
    player_list = []
    inventory_list = []
    for player in all_players:
        if player.inventory.is_open:
            player_list.append(player)
            inventory_list.append(player.inventory)
    random.shuffle(inventory_list)
    for i in range(len(player_list)):
        player_list[i].update_inventory(inventory_list[i])


def shuffle_fact(player: GameObjects.Player, all_players: list[GameObjects.Player], randomizer):
    player_list = []
    fact_list = []
    for player in all_players:
        if player.fact.is_open:
            player_list.append(player)
            fact_list.append(player.fact)
    random.shuffle(fact_list)
    for i in range(len(player_list)):
        player_list[i].update_fact(fact_list[i])
