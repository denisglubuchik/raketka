import random
import asyncio

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

from lexicon import LEXICON
from states import StartStates
from config import settings


router = Router()


def get_random_number():
    return random.uniform(1, 3)


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await message.bot.send_message(chat_id=settings.admin, text=f'Новый пользователь! {message.from_user.username}')
    button1 = InlineKeyboardButton(
        text='Зарегистрироваться на 1win',
        url=settings.ref,
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1]])

    await state.set_state(StartStates.wait_for_confirmation)

    photo = FSInputFile("1win.jpg")
    await message.bot.send_photo(chat_id=message.chat.id, photo=photo,
                                 caption=LEXICON["start"], reply_markup=keyboard)


@router.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer(text=LEXICON["rules"])


@router.message(F.photo, StateFilter(StartStates.wait_for_confirmation))
async def get_screen(message: Message, state: FSMContext):
    await message.copy_to(settings.admin)

    await state.set_state(StartStates.confirmed)
    button = InlineKeyboardButton(
        text='Правила пользования',
        callback_data='rules',
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await asyncio.sleep(10)
    await message.answer(text=LEXICON["confirmed"])
    await asyncio.sleep(5)
    await message.answer(text=LEXICON["welcome_to_team"], reply_markup=keyboard)


@router.callback_query(F.data == 'rules', StateFilter(StartStates.confirmed))
async def send_rules(callback, state: FSMContext):
    await callback.answer()
    button = InlineKeyboardButton(
        text='С правилами ознакомлен и согласен✅',
        callback_data='agreed',
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])

    await state.set_state(StartStates.agreed_with_rules)
    await callback.message.answer(text=LEXICON["rules"], reply_markup=keyboard)


@router.callback_query(F.data == 'agreed', StateFilter(StartStates.agreed_with_rules))
async def send_agreed(callback, state: FSMContext):
    await callback.answer()
    button = InlineKeyboardButton(
        text='Рассчитать сигнал📈',
        callback_data='signal'
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await callback.message.answer(text=LEXICON["work"], reply_markup=keyboard)


@router.callback_query(F.data == 'signal', StateFilter(StartStates.agreed_with_rules))
async def send_signal(callback, state: FSMContext):
    await callback.answer()
    num = get_random_number()
    button = InlineKeyboardButton(
        text='Рассчитать сигнал📈',
        callback_data='signal'
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await callback.message.answer(text=f"{num:.2f}x", reply_markup=keyboard)
