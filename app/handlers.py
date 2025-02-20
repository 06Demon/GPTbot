from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

from app.request import model

router = Router()


class Request(StatesGroup):
    request = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет, я бот, который сгенерирует картинку по твоему запросу",
        reply_markup=kb.home,
    )


@router.message(F.text == "Помощь")
async def cmd_help(message: Message):
    await message.answer(
        "Вот список доступных команд:\nПомощь - показывает доступные команды",
        reply_markup=kb.home,
    )


@router.message(F.text == "Сгенерировать")
async def cmd_generation(message: Message, state: FSMContext):
    await message.answer(
        "Введите запрос, по которому хотите сгенерировать картинку",
        reply_markup=kb.cancel,
    )
    await state.set_state(Request.request)


@router.message(F.text == "Завершить генерацию")
async def cancel_genersetion(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Генерация завершена, если вы желаете продолжить, то нажмине на соответствующую кнопку",
        reply_markup=kb.home,
    )


@router.message(Request.request)
async def request_processing(message: Message, state: FSMContext):
    await state.update_data(req=message.text)
    data = await state.get_data()
    response = model.chat(data["req"])
    await message.answer(
        f"Ответ нейросетки:\n{response.choices[0].message.content}",
        reply_markup=kb.cancel,
    )
