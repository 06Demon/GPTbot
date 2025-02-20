from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

home = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Помощь"), KeyboardButton(text="Сгенерировать")]],
    resize_keyboard=True,
    input_field_placeholder="Выбери команду...",
)

cancel = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Завершить генерацию")]],
    resize_keyboard=True,
)
