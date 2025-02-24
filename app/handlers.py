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


class Generation(StatesGroup):
    request_to_generation = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет, я бот, с помощью которого ты можешь общаться с GigaChat или генерировать картинки через Kandinsky 3.1\n Выбери соответсвующую команду для продолжения\n(Общение - общение с GigaChat\nСгенерировать картинку - генерация картинок с помощью Kandinsky 3.1)",
        reply_markup=kb.home,
    )


@router.message(F.text == "Помощь")
async def cmd_help(message: Message):
    await message.answer(
        "Вот список доступных команд:\nПомощь - показывает доступные команды\nСгенерировать картинку - начало работы с Kandinsky 3.1\nОбщение - начало работы с GigaChat\nЗавершить генерацию - прекращение работы с Kandinsky 3.1\nЗавершить общение - прекращение работы с GigaChat",
        reply_markup=kb.home,
    )


@router.message(F.text == "Сгенерировать картинку")
async def cmd_generation(message: Message, state: FSMContext):
    await message.answer(
        "Введите запрос, по которому хотите сгенерировать картинку\nЕсли вы передумали генерировать картинку, нажмите соответствующую кнопку ниже",
        reply_markup=kb.cancel_kand,
    )
    await state.set_state(Generation.request_to_generation)


@router.message(F.text == "Завершить генерацию")
async def cancel_generation(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Генерация завершена",
        reply_markup=kb.home,
    )


@router.message(Generation.request_to_generation)
async def generation_processing(message: Message, state: FSMContext):
    user_id = message.from_user.id

    await state.update_data(req=message.text)
    await message.answer("Подождите некоторое время", reply_markup=kb.cancel_kand)
    data = await state.get_data()

    uuid = api.generate(f"{data['req']}", model_id)
    images = api.check_generation(uuid)
    convert2img(user_id, images[0])

    image = FSInputFile(
        f"C:\\Lobovikov\\Programming\\PictureBot\\public\\{user_id}.webp"
    )
    await message.answer(
        "Ответ нейросетки:",
        reply_markup=kb.cancel_kand,
    )

    await message.answer_photo(photo=image)


@router.message(F.text == "Общение")
async def cmd_communication(message: Message, state: FSMContext):
    await message.answer(
        "Введите запрос для начала общения с GigaChat\nЕсли вы хотите прекратить общение, нажмите соответствующую кнопку ниже",
        reply_markup=kb.cancel_gigachat,
    )
    await state.set_state(Request.request)


@router.message(F.text == "Завершить общение")
async def cancel_generation(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Общение прекращено",
        reply_markup=kb.home,
    )


@router.message(Request.request)
async def communication_processing(message: Message, state: FSMContext):
    await state.update_data(req=message.text)
    data = await state.get_data()
    response = model.chat(data["req"])
    await message.answer(
        f"{response.choices[0].message.content}", reply_markup=kb.cancel_gigachat
    )
