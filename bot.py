from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os
import asyncio

# Загрузка переменных из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Определение состояний формы
class UserForm(StatesGroup):
    goal = State()
    age = State()
    height = State()
    weight = State()

# Команда /start запускает опрос
@dp.message(F.text == "/start")
async def start_form(message: Message, state: FSMContext):
    await message.answer("What is your goal? (e.g. gain, lose, maintain)")
    await state.set_state(UserForm.goal)

@dp.message(UserForm.goal)
async def get_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await message.answer("What is your age?")
    await state.set_state(UserForm.age)

@dp.message(UserForm.age)
async def get_age(message: Message, state: FSMContext):
    try:
        await state.update_data(age=int(message.text))
        await message.answer("What is your height (in centimeters)?")
        await state.set_state(UserForm.height)
    except ValueError:
        await message.answer("Please enter a valid number for age.")

@dp.message(UserForm.height)
async def get_height(message: Message, state: FSMContext):
    try:
        await state.update_data(height=int(message.text))
        await message.answer("What is your weight (in kilograms)?")
        await state.set_state(UserForm.weight)
    except ValueError:
        await message.answer("Please enter a valid number for height.")

@dp.message(UserForm.weight)
async def get_weight(message: Message, state: FSMContext):
    try:
        await state.update_data(weight=int(message.text))
        data = await state.get_data()

        await message.answer(f"""<b>Your goal:</b> {data['goal'].capitalize()}
<b>Age:</b> {data['age']} y.o.
<b>Height:</b> {data['height']} cm
<b>Weight:</b> {data['weight']} kg

A piece of advice for you:
- Drink more water
- Sleep at least 7–8 hours
- Strength training 3–5 times a week

If you want to get more information about healthy food or types of exercises, type this command: /plan
""")
        await state.clear()
    except ValueError:
        await message.answer("Please enter a valid number for weight.")

# План питания и тренировок
@dp.message(F.text == "/plan")
async def send_plan(message: Message):
    await message.answer("Example of the plan:\n\nBreakfast: Eggs + banana + oatmeal\nExercises: Shoulders + Chest\n")

# Точка входа
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
