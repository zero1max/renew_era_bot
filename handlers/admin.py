from aiogram import Router, F
from aiogram.types import Message
from database.db_users import get_all_users
import os
from .user import QuizStates
from loader import router_admin


@router_admin.message(QuizStates.WAITING_FOR_QUIZ_START, F.text == "View Results📊")
async def view_results(message: Message):
    if message.from_user.id != int(os.getenv("ADMIN_ID", "0")):
        await message.answer("❌ Sizda bu amalni bajarish huquqi yo‘q.")
        return

    users = get_all_users()
    if not users:
        await message.answer("Natijalar mavjud emas.")
        return

    # Foydalanuvchilarni to'g'ri javoblar soniga qarab saralash
    sorted_users = sorted(users, key=lambda x: x[2], reverse=True)

    text = "🏆 Foydalanuvchilar reytingi:\n\n"
    for i, u in enumerate(sorted_users, 1):
        text += f"{i}. @{u[1] or 'Anonymous'} (ID: {u[0]}): ✅ {u[3]}, ❌ {u[4]}\n"
    
    await message.answer(text)  