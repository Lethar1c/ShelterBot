import asyncio
import logging
import random
import sched

import aiogram.exceptions
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sqlite3
from aiogram import types, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, CommandObject

import Exceptions
import config

import GameObjects, Randomizer, Utils, Keyboards
from GameObjects import Player
from Game import Game
from typing import List, Dict
import time
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
logging.basicConfig(level=logging.INFO)

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

bot = Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
router = Router()
dp = Dispatcher()
dp.include_router(router)

game_waiting_time = 120.0  # время набора в игру
first_round_time = 120.0
opening_cards_time = 20.0
discussion_time = 120.0
voting_time = 15.0

min_players = 2
max_players = 16

scheduler = BackgroundScheduler()


class GameList:
    def __init__(self, game_list: List[Game]):
        self.game_list = game_list

    def create_new_game(self, game: Game):
        self.game_list.append(game)


games: Dict[int, GameList] = {}  # group id to game list of the group

games_id: Dict[int, Game] = {}

safe_modes: Dict[int, bool] = {}


async def open_card_round(game: Game, chat_id: int, game_id: int):
    if game.number_of_players > game.stay_in_shelter:
        game.step += 1
        await bot.send_message(chat_id=chat_id, text='Пора раскрыть одну вашу карту!',
                               reply_markup=Keyboards.go_to_bot)
        for player in game.player_list:
            shadow_card_list = player.get_shadow_cards_list()
            await bot.send_message(chat_id=player.player_id, text='Выберите карту, которую желаете раскрыть.',
                                   reply_markup=Keyboards.generate_shadow_card_keyboard(
                                       player_id=player.player_id,
                                       player_list=game.player_list,
                                       game_id=game_id,
                                       card_list=shadow_card_list,
                                       group_id=chat_id))
        await asyncio.sleep(opening_cards_time)
        await discussion(game, chat_id)
    else:
        await bot.send_message(chat_id=chat_id,
                               text='Похоже, мест в бункере теперь хватает всем. Пора теперь раскрыть все карты '
                                    'и узнать, достигнута ли главная цель - выжить...')
        text = ''
        for player in game.player_list:
            text = text + player.player_name + ':\n'
            cards = player.get_open_cards_list() + player.get_shadow_cards_list()
            for card in cards:
                text = text + f'{Utils.type_into_russian(card.type)}: ' + card.name + '\n'
            text += '\n'
        await bot.send_message(chat_id=chat_id, text=text)
        await bot.send_message(chat_id=chat_id, text='Счастливчики, чего тут таить...\n'
                                                     'Однако всем спасибо за упорное противостояние!')
        await bot.send_message(chat_id=chat_id, text='Игра окончена!')
        game.is_active = False


async def async_first_round(game: Game, chat_id: int, game_id: int):
    if not game.is_active:
        if game.number_of_players < min_players:
            await bot.send_message(chat_id=chat_id, text='Недостаточно игроков для начала...')
        else:
            game.is_active = True
            await bot.send_message(chat_id=chat_id, text='Игра началась!')
            game.generate_cards()
            await bot.send_message(chat_id=chat_id, text='На земле произошла катастрофа!')
            await bot.send_message(chat_id=chat_id, text=f'**{game.catastrophe.name}**\n\n{game.catastrophe.description}')
            await bot.send_message(chat_id=chat_id,
                                   text=f'Вы находитесь около спасительного бункера, но лишь {game.stay_in_shelter} чел. удастся спастись...\n\n'
                                        'Вот некоторые сведения об игроках.')
            players_occupations = ''
            for player in game.player_list:
                all_cards_list = player.get_shadow_cards_list()
                text = 'Вот твой сгенерированный персонаж:\n\n'
                for card in all_cards_list:
                    text = text + f'{Utils.type_into_russian(card.type)}: {card.name}\n'
                text += f'\nСпециальное условие: {player.special_condition.name}\n'
                text = text + '\n' + 'Докажи всем, что ты полезен для бункера!'
                await bot.send_message(chat_id=player.player_id, text=text)
                player.occupation.is_open = True
                players_occupations = players_occupations + player.player_name + ' - ' + f'**{player.occupation.name}**\n\n'
            await bot.send_message(chat_id=chat_id, text=players_occupations)
            await bot.send_message(chat_id=chat_id, text='Что ж... Вам самим решать, кто должен остаться в бункере.'
                                                         ' Да начнутся голодные игры!')
            await bot.send_message(chat_id=chat_id, text='Две минуты на обсуждение')
            await asyncio.sleep(first_round_time)
            await open_card_round(game, chat_id, game_id)
    else:
        pass


@dp.callback_query(F.data.startswith('open_'))
async def open_card_callback(callback: types.CallbackQuery):
    data = callback.data.split('_')
    game_id = int(data[1])
    player_number = int(data[2])
    card_type = data[3]
    game = games_id[game_id]
    group_id = int(data[4])
    print(game.player_list[player_number].get_open_cards_count())
    if game.player_list[player_number].get_open_cards_count() < game.step:
        game.player_list[player_number].open_card(card_type)
        await callback.answer()
        shadow_card_list = game.player_list[player_number].get_shadow_cards_list()
        await callback.message.edit_text(text='Выберите карту, которую желаете раскрыть.',
                                         reply_markup=Keyboards.generate_shadow_card_keyboard(
                                             player_id=callback.message.chat.id,
                                             player_list=game.player_list,
                                             game_id=game_id,
                                             card_list=shadow_card_list,
                                             group_id=group_id))
    else:
        await callback.answer(text='Вы уже раскрыли карту в этом раунде!', show_alert=True)


@dp.callback_query(F.data.startswith('spec_'))
async def using_special_condition(callback: types.CallbackQuery):
    data = callback.data.split('_')
    game_id = int(data[1])
    player_id = int(data[2])
    group_id = int(data[3])
    game = games_id[game_id]
    player_number = Utils.get_player_number_by_id(player_id, game.player_list)
    player = game.player_list[player_number]
    if player.special_condition.is_used or player in game.special_conditions_in_round.keys():
        await callback.answer(text='Ты уже использовал своё специальное условие!', show_alert=True)
    else:
        game.special_conditions_in_round[player] = player.special_condition
        await bot.send_message(chat_id=group_id,
                               text=f'Кто-то использовал специальное условие "{player.special_condition.name}".')
        await callback.answer(text='Специальное условие будет использовано после вскрытия карт текущего раунда.',
                              show_alert=True)


@dp.callback_query(F.data.startswith('vote_'))
async def vote_for_player_callback(callback: types.CallbackQuery):
    data = callback.data.split('_')
    game_id = int(data[1])
    voting_player_number = int(data[2])
    voted_player_number = int(data[3])
    game = games_id[game_id]
    if not game.player_list[voting_player_number].voted:
        game.player_list[voting_player_number].voted = True
        game.player_list[voted_player_number].votes += 1
        await callback.answer(text='Ваш голос принят.', show_alert=True)
    else:
        await callback.answer(text='Вы уже голосовали в этом раунде или время голосования истекло!', show_alert=True)


async def discussion(game: Game, chat_id: int):
    sc_list = game.special_conditions_in_round
    if len(sc_list.keys()) == 0:
        await bot.send_message(chat_id=chat_id, text='В этом раунде специальные условия не были использованы...')
    else:
        for player in sc_list.keys():
            try:
                sc_list[player].run(player, game.player_list, game.randomizer)
            except Exceptions.SpecialConditionIsAlreadyUsed:
                await bot.send_message(chat_id=player.player_id,
                                       text='Вы уже использовали специальное условие в этой игре!')
        for player in game.player_list:
            await bot.send_message(chat_id=player.player_id,
                                   text='После использования специальных условий произошли некоторые '
                                        'изменения. Познакомься со своей новой личностью.')
            all_open_cards_list = player.get_open_cards_list()
            all_shadow_cards_list = player.get_shadow_cards_list()
            text = 'Открытые карты:\n'
            for card in all_open_cards_list:
                text = text + f'{Utils.type_into_russian(card.type)}: {card.name}\n'
            text += '\nТвоя тёмная сторона:\n'
            for card in all_shadow_cards_list:
                text = text + f'{Utils.type_into_russian(card.type)}: {card.name}\n'
            if player.special_condition.is_used:
                text += '\nСпециальное условие использовано'
            else:
                text += f'\nСпециальное условие: {player.special_condition.name}\n'
            await bot.send_message(chat_id=player.player_id, text=text)

    for player in game.player_list:
        while len(player.get_open_cards_list()) < game.step:
            shadow_card_list = player.get_shadow_cards_list()
            shadow_card_list[random.randint(0, len(shadow_card_list)-1)].is_open = True
    await bot.send_message(chat_id=chat_id, text='Пора узнать немного больше информации об игроках...')
    text = ''
    for player in game.player_list:
        text += f'{player.player_name}:\n'
        for card in player.get_open_cards_list():
            text = text + f'{Utils.type_into_russian(card.type)}: ' + card.name + '\n'
        text += '\n'
    await bot.send_message(chat_id=chat_id, text=text)
    await bot.send_message(chat_id=chat_id, text='Две минуты на обсуждение!')
    await asyncio.sleep(discussion_time)
    await voting_round(game, chat_id)


async def voting_round(game: Game, chat_id: int):
    await bot.send_message(chat_id=chat_id, text='Пришло время голосовать, кого вышвырнуть из бункера...',
                           reply_markup=Keyboards.go_to_bot)
    for player in game.player_list:
        player.voted = False
        player.votes = 0
    for player in game.player_list:
        await bot.send_message(chat_id=player.player_id, text='За кого голосуем?',
                               reply_markup=Keyboards.generate_voting_keyboard(player_id=player.player_id,
                                                                               player_list=game.player_list,
                                                                               game_id=game.game_id))
    await asyncio.sleep(voting_time)
    await kick_player(game, chat_id)


async def kick_player(game: Game, chat_id: int):
    votes = []
    for player in game.player_list:
        player.voted = True
        votes.append(player.votes)
    max_votes = max(votes)
    elimination_list = []
    for player in game.player_list:
        if player.votes == max_votes:
            elimination_list.append(player)
    eliminating_player: Player = game.player_list[0]
    if len(elimination_list) == 1:
        eliminating_player = elimination_list[0]
    if len(elimination_list) >= 2:
        eliminating_player = elimination_list[random.randint(0, len(elimination_list)-1)]
        await bot.send_message(chat_id=chat_id, text='Голосование завершилось неоднозначно. '
                                                     'Главный голос за бортовым компьютером бункера...')
    await bot.send_message(chat_id=chat_id,
                           text=f'Голосование окончено. Выбывает игрок {eliminating_player.player_name}\n\n'
                                f'Познакомимся с его характеристиками')
    cards = eliminating_player.get_open_cards_list() + eliminating_player.get_shadow_cards_list()
    text = ''
    for card in cards:
        text = text + f'{Utils.type_into_russian(card.type)}: ' + card.name + '\n'
    text = text + '\n' + 'Удачного выживания в лесу, лузер!'
    await bot.send_message(chat_id=eliminating_player.player_id, text=f'Тебя выдворили из бункера! '
                                                                      f'Удачного выживания в лесу, лузер!')
    game.eliminate_player(eliminating_player.player_id)
    await bot.send_message(chat_id=chat_id, text=text)
    await open_card_round(game=game, chat_id=chat_id, game_id=game.game_id)
    await asyncio.sleep(opening_cards_time)


@router.message(Command('start'))
async def start_handler(message: Message):
    if message.chat.id > 0:
        await message.answer('Привет! Я бот для игры в бункер! Добавь меня в группу и я начну свою работу!')
    else:
        if message.chat.id not in safe_modes.keys():
            safe_modes[message.chat.id] = True
        if message.chat.id not in games.keys():
            games[message.chat.id] = GameList([])
            game = Game(catastrophe=Randomizer.GameRandomizer.generate_catastrophe(),
                        player_list=[],
                        randomizer=Randomizer.GameRandomizer(safe_mode=safe_modes[message.chat.id]),
                        game_id=len(games_id),
                        group_id=message.chat.id)
            games[message.chat.id].create_new_game(game)
            games_id[len(games_id)] = game
            end_registration_time = datetime.datetime.fromtimestamp(time.time()+game_waiting_time).time()
            await message.answer(text=f'Начинается набор в игру! Окончание регистации в '
                                      f'{str(end_registration_time)[0:8]}',
                                 reply_markup=Keyboards.generate_join_keyboard(
                                     message.chat.id, len(games[message.chat.id].game_list)))
            await asyncio.sleep(game_waiting_time)
            await async_first_round(games[message.chat.id].game_list[-1], message.chat.id,
                                    len(games[message.chat.id].game_list)-1)
        elif time.time() - games[message.chat.id].game_list[-1].timer < game_waiting_time:
            await message.answer(text='Набор в игру уже ведётся!')
        elif games[message.chat.id].game_list[-1].is_active:
            await message.answer(text='Игра уже идёт!')
        else:
            game = Game(catastrophe=Randomizer.GameRandomizer.generate_catastrophe(),
                        player_list=[],
                        randomizer=Randomizer.GameRandomizer(safe_mode=safe_modes[message.chat.id]),
                        game_id=len(games_id),
                        group_id=message.chat.id)
            games[message.chat.id].create_new_game(game)
            games_id[len(games_id)] = game
            await message.answer(text='Начинается набор в игру!',
                                 reply_markup=Keyboards.generate_join_keyboard(
                                     message.chat.id, len(games[message.chat.id].game_list)))
            await asyncio.sleep(game_waiting_time)
            await async_first_round(games[message.chat.id].game_list[-1], message.chat.id,
                                    len(games[message.chat.id].game_list) - 1)


@dp.message(CommandStart(deep_link=True))  # deep link
async def handler(msg: Message, command: CommandObject):
    args = command.args
    if args.startswith('game'):  # обработка команды присоединения к игре
        try:
            args_list = args.split('_')
            group_id = int(args_list[1])
            game_id = int(args_list[2])
            game_index = game_id - 1
            if games[group_id].game_list[game_index].is_active:
                await msg.answer('Игра уже началась!')
            else:
                if msg.from_user.id not in games[group_id].game_list[game_index].get_player_id_list():
                    games[group_id].game_list[game_index].add_player(Player(msg.from_user.id, msg.from_user.full_name))
                    await msg.answer(f'Ты присоединился к игре №{game_id}!')
                    await bot.send_message(chat_id=group_id, text=f'{msg.from_user.full_name} присоединился к игре.')
                    if games[group_id].game_list[game_index].number_of_players == max_players:
                        await async_first_round(games[group_id].game_list[-1], group_id,
                                                len(games[group_id].game_list) - 1)
                else:
                    await msg.answer(f'Ты уже состоишь в игре №{game_id}!')
        except ValueError as e:
            logging.log(logging.INFO, 'Invalid link for a game')
            await msg.answer('Недействительная ссылка на игру!')


@router.message(Command('begin'))
async def begin_handler(message: Message):  # досрочно начать игру
    if message.chat.id < 0:
        if message.chat.id in games.keys():
            if not games[message.chat.id].game_list[-1].is_active \
               and time.time() - games[message.chat.id].game_list[-1].timer < game_waiting_time:
                await async_first_round(games[message.chat.id].game_list[-1], message.chat.id,
                                        len(games[message.chat.id].game_list) - 1)
    else:
        await message.answer('Добавь меня в группу, чтобы я заработал!')


@router.message(Command('enable_safe_mode'))
async def enable_safe_mode(message: Message):
    if message.chat.id < 0:
        safe_modes[message.chat.id] = True
        await message.answer('Безопасный режим включен')
    else:
        await message.answer('Добавь меня в группу, чтобы я заработал!')


@router.message(Command('disable_safe_mode'))
async def disable_safe_mode(message: Message):
    if message.chat.id < 0:
        safe_modes[message.chat.id] = False
        await message.answer('Безопасный режим выключен')
    else:
        await message.answer('Добавь меня в группу, чтобы я заработал!')


@router.message()
async def message_handler(message: Message):
    if message.chat.id > 0:
        await message.answer('Добавь меня в группу, чтобы я заработал!')
    else:
        if message.chat.id in games.keys():
            if games[message.chat.id].game_list[-1].is_active:
                if message.from_user.id not in games[message.chat.id].game_list[-1].get_player_id_list():
                    await message.delete()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
