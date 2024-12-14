from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from database import create_table, insert_row_employee, fetch_all_courses
from dotenv import load_dotenv
import os


load_dotenv()

TOKEN = os.getenv('TOKEN')
ADMIN_ID = 5167032738

bot = Bot(token=TOKEN)
dp = Dispatcher()



class CourseStates(StatesGroup):
    name = State()
    price = State()
    description = State()
    teacher_info = State()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    keybord1 = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="O'quv kurslar")],
            [KeyboardButton(text="Bizning afzalliklar")],
            [KeyboardButton(text="Kurs qo'shish")]
        ],
        resize_keyboard=True
    )
    await message.reply(text=f"{message.from_user.first_name}\nAssalomu alaykum botimizga hush kelibsiz/bizning o'quv markaz eng zor", reply_markup=keybord1)
    create_table()


@dp.message(lambda message: message.text == "O'quv kurslar")
async def courses_handler(message: Message):
    db_courses = fetch_all_courses()  
    if db_courses:
        inline_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=course[0], callback_data=f"course_{i}")]
                for i, course in enumerate(db_courses)
            ]
        )
        await message.reply("Kurslar ro'yxati:", reply_markup=inline_kb)
    else:
        await message.reply("Hozircha kurslar yo'q.")


@dp.callback_query(lambda query: query.data.startswith("course_"))
async def course_details_handler(query: CallbackQuery):
    db_courses = fetch_all_courses()  # Kurslarni qayta yuklaymiz
    course_index = int(query.data.split("_")[1])  
    if course_index < len(db_courses):
        course = db_courses[course_index]
        course_details = (
            f"Kurs nomi: {course[0]}\n"
            f"Narxi: {course[1]}\n"
            f"Tavsifi: {course[2]}\n"
            f"O'qituvchi haqida: {course[3]}"
        )
        await query.message.reply(course_details)
    else:
        await query.message.reply("Bunday kurs mavjud emas.")


@dp.message(lambda message: message.text == "Bizning afzalliklar")
async def benefits_handler(message: Message):
    await message.reply("Bizning afzalliklarimiz:\n- Malakali o'qituvchilar\n- Amaliy darslar\n- Zamonaviy materiallar")


@dp.message(lambda message: message.text == "Kurs qo'shish" )
async def add_course_handler(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await message.reply("Kurs nomini kiriting:")
        await state.set_state(CourseStates.name)
    else:
        await message.reply("Uzur!\nSiz bu bo'limdan foydalana o'lamaysiz")


@dp.message(CourseStates.name)
async def add_course_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply("Kurs narxini kiriting:")
    await state.set_state(CourseStates.price)


@dp.message(CourseStates.price)
async def add_course_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.reply("Kurs tavsifini kiriting:")
    await state.set_state(CourseStates.description)


@dp.message(CourseStates.description)
async def add_course_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.reply("O'qituvchi haqida ma'lumot kiriting:")
    await state.set_state(CourseStates.teacher_info)


@dp.message(CourseStates.teacher_info)
async def add_course_teacher_info(message: Message, state: FSMContext):
    await state.update_data(teacher_info=message.text)
    data = await state.get_data()
    insert_row_employee(data['name'], data['price'], data['description'], data['teacher_info'])


    await message.reply(f"Kurs muvaffaqiyatli qo'shildi!\nName: {data["name"]}\nPrice: {data["price"]}\nDescraption: {data['description']}\nTeacher_info: {data['teacher_info']}")
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
