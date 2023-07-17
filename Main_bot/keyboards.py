from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton 


main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(KeyboardButton("📚 Info", )).insert("💻 About me").add("👨‍💻 Product list").add("🔐 Admin panel")


product_keyboard = InlineKeyboardMarkup(row_width=2)
product_keyboard.add(InlineKeyboardButton(text="🏔 Истоки", callback_data="@istoki"),
                      InlineKeyboardButton(text="🌊 Набережная", callback_data="@seafront"), 
                      InlineKeyboardButton(text="🍃 Труд", callback_data="@work"))


cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add(KeyboardButton("❌ Cancel")).insert(KeyboardButton("↖️ Вернуться к выбору"))


enter_istoki = InlineKeyboardMarkup(row_width=1)
enter_istoki.add(InlineKeyboardButton(text="💰 Купить пароли", callback_data="istoki"))

enter_seafront = InlineKeyboardMarkup(row_width=1)
enter_seafront.add(InlineKeyboardButton(text="💰 Купить пароли", callback_data="seafront"))

enter_work = InlineKeyboardMarkup(row_width=1)
enter_work.add(InlineKeyboardButton(text="💰 Купить пароли", callback_data="work"))


admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add(KeyboardButton("📚 Info", )).insert(KeyboardButton("💻 About me")
).add(KeyboardButton("👨‍💻 Product list")).add(KeyboardButton("🔐 Admin panel")
).add(KeyboardButton("🔧 Добавить локацию")).add(KeyboardButton("💰 Добавить пароль"))



