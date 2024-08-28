import GameObjects
import Exceptions


def type_into_russian(card_type: str):
    if card_type == 'occupation':
        return 'Профессия'
    elif card_type == 'biology':
        return 'Биологические данные'
    elif card_type == 'character':
        return 'Характер'
    elif card_type == 'health':
        return 'Здоровье'
    elif card_type == 'hobby':
        return 'Хобби'
    elif card_type == 'phobia':
        return 'Фобия'
    elif card_type == 'inventory':
        return 'Багаж'
    elif card_type == 'fact':
        return 'Факт'
    else:
        return ''


def search_player_by_id(player_id: int, player_list: list[GameObjects.Player]):
    for player in player_list:
        if player_id == player.player_id:
            return player
    raise Exceptions.PlayerNotFound


def get_player_number_by_id(player_id: int, player_list: list[GameObjects.Player]):
    i = 0
    for player in player_list:
        if player_id == player.player_id:
            return i
        i += 1
    raise Exceptions.PlayerNotFound


def vote_for_player(player_id: int, player_list: list[GameObjects.Player]):
    search_player_by_id(player_id, player_list).votes += 1


def list_of_max_voted_players(player_list: list[GameObjects.Player]):
    res = []
    max_votes = -1
    for player in player_list:
        if player.votes > max_votes:
            res = [player]
        if player.votes == max_votes:
            res.append(player)
    return res
