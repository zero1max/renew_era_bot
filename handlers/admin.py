from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.main import get_main_keyboard, get_question_keyboard
from database.db_users import add_user, update_score
from quiz_data import questions
import os
import random
from loader import router_user


class QuizStates(StatesGroup):
    WAITING_FOR_QUIZ_START = State()
    ANSWERING_QUESTION = State()


@router_user.message(F.text == "/start")
async def start_cmd(message: Message, state: FSMContext):
    add_user(message.from_user.id, message.from_user.username)
    is_admin = message.from_user.id == int(os.getenv("ADMIN_ID", "0"))
    await message.answer("Salom! Tarix bo‘yicha viktorinamizga xush kelibsiz!", reply_markup=get_main_keyboard(is_admin))
    await state.set_state(QuizStates.WAITING_FOR_QUIZ_START)


@router_user.message(QuizStates.WAITING_FOR_QUIZ_START, F.text == "Bilimni sinash📚")
async def start_quiz(message: Message, state: FSMContext):
    # Savollar ro'yxatini tasodifiy aralashtirish
    shuffled_questions = questions.copy()
    random.shuffle(shuffled_questions)
    await state.update_data(current_question=0, shuffled_questions=shuffled_questions)
    await send_question(message, state)


async def send_question(message, state: FSMContext):
    data = await state.get_data()
    idx = data.get("current_question", 0)
    shuffled_questions = data.get("shuffled_questions", questions)

    if idx >= len(shuffled_questions):
        await message.answer("Viktorina tugadi! /start buyrug‘i bilan qayta boshlang.", reply_markup=get_main_keyboard())
        await state.clear()
        return

    question = shuffled_questions[idx].copy()
    
    # Javob variantlarini tasodifiy aralashtirish
    temp = list(zip(question["options"], [i == question["correct"] for i in range(len(question["options"]))]))
    random.shuffle(temp)
    question["options"], correct_flags = zip(*temp)
    question["correct"] = correct_flags.index(True)

    await message.answer(question["question"], reply_markup=get_question_keyboard(question["options"]))
    await state.update_data(current_question=idx, correct_answer=question["correct"])
    await state.set_state(QuizStates.ANSWERING_QUESTION)


@router_user.callback_query(QuizStates.ANSWERING_QUESTION)
async def handle_answer(callback: CallbackQuery, state: FSMContext):
    selected = int(callback.data.split("_")[1])
    data = await state.get_data()
    correct = data["correct_answer"]

    update_score(callback.from_user.id, selected == correct)

    await callback.answer("✅ To‘g‘ri!" if selected == correct else "❌ Noto‘g‘ri.")
    await callback.message.delete()  # Eski savol xabarini o‘chiramiz

    await state.update_data(current_question=data["current_question"] + 1)
    await send_question(callback.message, state)