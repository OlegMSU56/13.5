from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = 'ключ'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button1)
kb.add(button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Информация о боте\n\nЭтот бот предназначен для расчетов калорий, '
                         'основанных на вашей банковской карте\n\n'
                         '(это шутка! НЕ передавайте НИКОМУ данные своей банковской карты\n'
                         'этими данными могут воспользоваться мошенники)', reply_markup=kb)

@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state):
    try:
        age = int(message.text)
        if age <= 0:
            raise ValueError("Возраст должен быть положительным числом.")
        await state.update_data(age=age)
        await message.answer('Введите свой рост в см:')
        await UserState.growth.set()
    except ValueError as e:
        await message.answer(f"Ошибка ввода возраста: {e}\nПопробуйте снова:")
        return


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state):
    try:
        growth = int(message.text)
        if growth <= 0:
            raise ValueError('Рост должен быть положительным числом.')
        await state.update_data(growth=message.text)
        await message.answer('Введите свой вес в кг:')
        await UserState.weight.set()
    except ValueError as e:
        await message.answer(f"Ошибка ввода веса: {e}\nПопробуйте снова:")
        return


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state):
    try:
        weight = int(message.text)
        if weight <= 0:
            raise ValueError('Вес должен быть положительным числом.')
        await state.update_data(weight=message.text)
        data = await state.get_data()
        age = int(data['age'])
        growth = int(data['growth'])
        weight = int(data['weight'])
        calories = (10 * weight) + (6.25 * growth) - (5 * age) + 5
        await message.answer(f'Ваша норма калорий: {calories:.2f}')
        await state.finish()
    except ValueError as e:
        await message.answer(f"Ошибка ввода роста: {e}\nПопробуйте снова:")
        return

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
