from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import Utils


def generate_join_keyboard(group_id: int, game_id: int):
    join_keyboard = InlineKeyboardBuilder().button(text='Присоединиться',
                                                   url=f'https://t.me/bunker2play_bot?start=game_{group_id}_{game_id}')
    return join_keyboard.as_markup()


go_to_bot = InlineKeyboardBuilder().button(text='Перейти в бота',
                                           url='https://t.me/bunker2play_bot').as_markup()


def generate_shadow_card_keyboard(player_id: int, player_list: list, game_id: int, card_list: list, group_id: int):
    player_number = Utils.get_player_number_by_id(player_id, player_list)
    keyboard = InlineKeyboardBuilder()
    for card in card_list:
        keyboard.button(text=Utils.type_into_russian(card.type),
                        callback_data=f'open_{game_id}_{player_number}_{card.type}_{group_id}')
    if not player_list[player_number].special_condition.is_used:
        keyboard.button(text='ИСПОЛЬЗОВАТЬ СПЕЦИАЛЬНОЕ УСЛОВИЕ', callback_data=f'spec_{game_id}_{player_id}_{group_id}')
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()


def generate_voting_keyboard(player_id: int, player_list: list, game_id: int):
    keyboard = InlineKeyboardBuilder()
    i = 0
    for player in player_list:
        keyboard.button(text=player.player_name,
                        callback_data=f'vote_{game_id}_{Utils.get_player_number_by_id(player_id, player_list)}_{i}')
        i += 1
    return keyboard.adjust(1, repeat=True).as_markup()
