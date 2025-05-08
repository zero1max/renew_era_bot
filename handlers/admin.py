from aiogram import Router, F
from aiogram.types import Message
from database.db_users import get_all_users
import os
from .user import QuizStates
from loader import router_admin


@router_admin.message(QuizStates.WAITING_FOR_QUIZ_START, F.text == "View Results")
async def view_results(message: Message):
    if message.from_user.id != int(os.getenv("ADMIN_ID", "0")):
        await message.answer("❌ Sizda bu amalni bajarish huquqi yo‘q.")
        return

    users = get_all_users()
    if not users:
        await message.answer("Natijalar mavjud emas.")
        return

    text = "📊 Foydalanuvchilar natijalari:\n"
    for u in users:
        text += f"@{u[1] or 'Anonymous'} (ID: {u[0]}): ✅ {u[2]}, ❌ {u[3]}\n"
    await message.answer(text)
