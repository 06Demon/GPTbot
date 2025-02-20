from aiogram import Router, F
from aiogram.methods import SendPhoto
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

from app.request import model, convert2img
from app.request import Text2ImageAPI


router = Router()

api = Text2ImageAPI(
    "https://api-key.fusionbrain.ai/",
    "32F203712629E1BA3D92157F36B2F99E",
    "E2C2F5E6C21918DE690011D8D44E05C8",
)
model_id = api.get_model()


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
    await message.answer("Подождите некоторое время", reply_markup=kb.cancel)
    data = await state.get_data()

    uuid = api.generate(f"{data['req']}", model_id)
    images = api.check_generation(uuid)
    convert2img(images[0])

    image = FSInputFile("C:\\Lobovikov\\Programming\\PictureBot\\img.webp")
    await message.answer(
        "Ответ нейросетки:",
        reply_markup=kb.cancel,
    )
    await message.answer_photo(image)
