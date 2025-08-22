from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def language_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="English", callback_data="lang_en"))
    kb.add(InlineKeyboardButton(text="Serbian", callback_data="lang_sr"))
    return kb
