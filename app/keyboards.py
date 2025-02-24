from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

home = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Общение"), KeyboardButton(text="Сгенерировать картинку")],
        [KeyboardButton(text="Помощь")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите необходимую AI",
)

cancel_kand = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Завершить генерацию")]],
    resize_keyboard=True,
)


cancel_gigachat = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Завершить общение")]],
    resize_keyboard=True,
)
