import random

import GameObjects
import Game
import Randomizer
import time

print(time.time())

"""
def func(all_players: list[GameObjects.Player], open_cards: list[GameObjects.Player]):
    print(all_players[0].hobby)
    all_players[0].update_hobby('new hobby')
    print(all_players[0].hobby)


special_condition = GameObjects.SpecialCondition('name', func)
randomizer = Randomizer.GameRandomizer(safe_mode=False)

player_list = []

n = 5

for i in range(n):
    player = GameObjects.Player(i+1, f'name{i+1}', 'occupation', 'biology', 'character',
                                'health', 'hobby', 'phobia', 'inventory', 'fact', special_condition)
    player_list.append(player)

catastrophe = GameObjects.Catastrophe('Catastropha1', 'AAAAAAAAAA')

game = Game.Game(catastrophe, player_list, randomizer)
game.generate_cards()
for player in game.player_list:
    print(f'{player.player_id}. {player.occupation.name}, {player.biology.name}, {player.character.name}, {player.health.name}, '
          f'{player.hobby.name}, {player.phobia.name}, {player.inventory.name}, {player.fact.name}, {player.special_condition.name}')

a = random.randint(1, n)
game.eliminate_player(a)

print()

for player in game.player_list:
    game.open_card(player, 'fact')
    game.open_card(player, 'biology')
    print(f'{player.player_id}. {player.occupation.name}, {player.biology.name}, {player.character.name}, {player.health.name}, '
          f'{player.hobby.name}, {player.phobia.name}, {player.inventory.name}, {player.fact.name}, {player.special_condition.name}')

l = game.get_open_cards_list()

for player in l.keys():
    print(f'{player.player_id}. {player.player_name}: ')
    for card in l[player]:
        print(f'  {card}')
    print()
game.player_list[0].special_condition.run(player_list[0], player_list, randomizer)
print()

for player in game.player_list:
    print(f'{player.player_id}. {player.occupation.name}, {player.biology.name}, {player.character.name}, {player.health.name}, '
          f'{player.hobby.name}, {player.phobia.name}, {player.inventory.name}, {player.fact.name}, {player.special_condition.name}')
for i in range(n):
    player_list[i].update_occupation(randomizer.generate_occupation())
    player_list[i].update_hobby(randomizer.generate_hobby())
    player_list[i].update_biology(randomizer.generate_biology())
    player_list[i].update_character(randomizer.generate_character())
    player_list[i].update_fact(randomizer.generate_fact())
    player_list[i].update_health(randomizer.generate_health())
    player_list[i].update_inventory(randomizer.generate_inventory())
    player_list[i].update_phobia(randomizer.generate_phobia())
open_cards = player_list[0:3]
for i in range(n):
    player = player_list[i]
    print(f'{player.player_id}. {player.occupation}, {player.biology}, {player.character}, {player.health}, '
          f'{player.hobby}, {player.phobia}, {player.inventory}, {player.fact}')
print()
SpecialConditions.shuffle_occupation(1, player_list)
SpecialConditions.shuffle_health(1, player_list)
SpecialConditions.shuffle_phobia(1, player_list)
for i in range(n):
    player = player_list[i]
    print(f'{player.player_id}. {player.occupation}, {player.biology}, {player.character}, {player.health}, '
          f'{player.hobby}, {player.phobia}, {player.inventory}, {player.fact}')
"""