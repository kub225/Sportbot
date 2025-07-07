from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import os
import asyncio
from aiogram.fsm.context import FSMContext

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
class UserForm(StatesGroup):
    goal = State()
    age = State()
    height = State()
    weight = State()
@dp.message(UserForm.age)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("What is your age?")
    await state.set_state(UserForm.age)
@dp.message(UserForm.height)
async def get_height(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("What is your height(in centimeters)?")
    await state.set_state(UserForm.height)
@dp.message(UserForm.weight)
async def get_weight(message: Message, state: FSMContext):
    await state.update_data(height=int(message.text))
    await message.answer("What is your weight(in kilograms)?")
    await state.get_state(UserForm.weight)
@dp.message(UserForm.goal)
async def get_goal(message: Message, state: FSMContext):
    await state.update_data(goal=int(message.text))
    data = await state.get_data()

    await message.answer(f"""<b>Your goal:</b> {data['goal'].capitalize()}
<b>Age:</b> {data['age']} y.o.
<b>Height</b> {data['height']} cm.
<b>Weight</b> {data['weight']} kg.

 A piece of advice for you:
 -Drink more water
 -Sleep at least 7-8 hours.
 -Strength training 3-5 times a week
 If you want to get more information about healthy food or types of exercises, type this command: /plan""")
    await state.clear()
@dp.message(F.text == '/plan')
async def send_plan(message: Message):
    await message.answer("Example of the plan:\n\n Breakfast: Egg+banana+oatmeal\n Exercises: Shoulders+Chest\n")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
