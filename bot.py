import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# === Загружаем переменные окружения ===
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Проверка, что токен загружен
if not TOKEN:
    raise ValueError("❌ Ошибка: BOT_TOKEN не найден в .env файле!")

if not ADMIN_ID:
    raise ValueError("❌ Ошибка: ADMIN_ID не найден в .env файле!")

# === Инициализация бота и диспетчера ===
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# === Клавиатура главного меню ===
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📚 Лабораторные работы"),
            KeyboardButton(text="📖 Лекции"),
            KeyboardButton(text="ℹ️ О курсе"),
        ],
        [
            KeyboardButton(text="❓ Задать вопрос преподавателю")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# === Словарь с ссылками на лабораторные работы ===
lab_links = {
    "1": "Основы работы с Git и GitHub - https://drive.google.com/file/d/xxx/view",
    "2": "Совместная работа в GitHub (форки, pull request) - https://drive.google.com/file/d/yyy/view",
    "3": "Гибкие методологии Scrum и Kanban - https://github.com/example/lab3.pdf",
    "4": "Код-стиль и оформление кода - https://example.com/lab4.pdf",
    "5": "Тестирование программного кода - https://example.com/lab5.pdf",
    "6": "CI/CD в разработке - https://example.com/lab6.pdf",
    "7": "Отладка кода - https://example.com/lab7.pdf",
    "8": "Финальный проект и презентация - https://example.com/lab8.pdf",
}

# === Словарь с ссылками на лекции ===
lecture_links = {
    "1": "Введение в технологии программирования - https://example.com/lecture1.pdf",
    "2": "Жизненный цикл разработки ПО - https://example.com/lecture2.pdf",
    "3": "Парадигмы программирования - https://example.com/lecture3.pdf",
    "4": "Основы командной разработки - https://example.com/lecture4.pdf",
    "5": "Инструменты командной работы - https://example.com/lecture5.pdf",
    "6": "Обеспечение качества ПО - https://example.com/lecture6.pdf",
    "7": "Тестирование ПО - https://example.com/lecture7.pdf",
    "8": "Отладка и автоматизация тестирования - https://example.com/lecture8.pdf",
}

# === Обработчик команды /start ===
@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в Telegram-бот курса 'Технология разработки программного обеспечения' (ТРПО) "
        "Института 'Высшая ИТ-школа' Костромского Государственного Университета! 🎓\n\n"
        "Этот курс разработан специально для студентов, чтобы освоить современные технологии командной разработки ПО, "
        "контроль версий, тестирование, CI/CD и другие важные аспекты программной инженерии.\n\n"
        "Выберите нужную опцию в меню ниже. 👇",
        reply_markup=menu_keyboard
    )

# === Обработчик команды /lectures ===
@router.message(F.text == "📖 Лекции")
async def send_lectures_list(message: types.Message):
    lecture_list = "\n".join([f"🎓 Лекция {num}: {desc}" for num, desc in lecture_links.items()])
    await message.answer(f"Вот список доступных лекций:\n\n{lecture_list}\n\nВведите номер лекции для получения ссылки.")

# === Обработчик выбора лекции ===
@router.message(F.text.regexp(r"^\d+$"))
async def send_lecture_link(message: types.Message):
    lecture_number = message.text.strip()
    if lecture_number in lecture_links:
        await message.answer(f"📖 Лекция {lecture_number}: {lecture_links[lecture_number]}")
    else:
        await message.answer("⚠️ Такой лекции нет. Попробуйте ввести номер от 1 до 8.")

# === Обработчик кнопки 'О курсе' ===
@router.message(F.text == "ℹ️ О курсе")
async def send_course_info(message: types.Message):
    await message.answer(
        "📌 *Курс: Технология разработки программного обеспечения*\n\n"
        "Этот курс создан специально для студентов Института 'Высшая ИТ-школа' "
        "Костромского Государственного Университета.\n\n"
        "📖 *Автор курса*: к.т.н., доцент кафедры ИСТ Мозохин Александр Евгеньевич.\n\n"
        "📚 В рамках курса студенты изучат методы разработки ПО, командную работу, тестирование, CI/CD, "
        "а также научатся разрабатывать и отлаживать программные продукты с использованием современных инструментов."
    )

# === Функция запуска бота ===
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

# === Запуск бота ===
if __name__ == "__main__":
    asyncio.run(main())
