import os


import keyboards as kb
import database as db


from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.message import ContentType


from dotenv import load_dotenv


HELP_BOARD = """
📚 Info - показывает это табло.
👨‍💻 Product list - показывает список товаров.
💻 About me - информация обо мне.
🔐 Admin panel - вызывает админ панель (доступно не всем).
"""



# ///////////////////// data ///////////////////////////


content_dict = {"@istoki": "../data/images/istoki.jpg",
                "@seafront": "../data/images/seafront.jpg",
                "@work": "../data/images/work.jpeg"} 

products = 0


# //////////////////// init bot ///////////////////////


load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode="HTML")
dp = Dispatcher(bot=bot, storage=MemoryStorage())


class SaveData:
    item = ""

async def on_startup(_): 
    global products   
    products = db.db_start()
    print("/Bot started")



@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(f"Привет, <b>{message.from_user.first_name}</b>. Это магазин по продаже паролей от WiFi точек по всему городу. ", reply_markup=kb.main_keyboard)
    
@dp.message_handler(text=["exit"])
async def exit(message: types.Message):

    raise SystemExit()


@dp.message_handler(text=["👨‍💻 Product list", "↖️ Вернуться к выбору"])
async def product_list(message: types.Message):
    with open("../data/images/preview_list.jpg", "rb") as file:
        await message.answer_photo(photo=file, caption="<em>Выбери интересующее <b>тебя</b> место</em>", reply_markup=kb.product_keyboard)


@dp.message_handler(text=["📚 Info", "❌ Cancel"])
async def info(message: types.Message):
    await message.reply(HELP_BOARD, reply_markup=kb.main_keyboard)


@dp.message_handler(text="🔐 Admin panel")
async def admin_panel(message: types.Message):
    if message.from_user.id == int(os.getenv("ADMIN_ID")):
        await message.answer("вы вошли как root", reply_markup=kb.admin_panel)
    else:
        await message.answer("Вы не являетесь создателем бота, root$elliot")




# ///////////////////////// CALLBACK QUERY //////////////////////////////






@dp.callback_query_handler(text=["@istoki", "@seafront", "@work"])
async def choice_path(query: types.CallbackQuery):

    await query.message.answer("Секунду...", reply_markup=kb.cancel)
    item = str(query.data)[1:]
    length_passwords = str(products[item+"_count"])

    if query.data in content_dict:
        with open(content_dict[query.data], "rb") as file:
            
            
            if item == "istoki":
                await query.message.answer_photo(photo=file, caption=str(products[item][1].replace("*", length_passwords)),  reply_markup=kb.enter_istoki)
            
            elif item == "seafront":
                await query.message.answer_photo(photo=file, caption=str(products[item][1].replace("*", length_passwords)),  reply_markup=kb.enter_seafront)

            elif item == "work":
                await query.message.answer_photo(photo=file, caption=str(products[item][1].replace("*", length_passwords)),  reply_markup=kb.enter_work)
    
    SaveData.item = item
    
    

@dp.callback_query_handler(text=["istoki", "seafront", "work"])
async def buy(query: types.CallbackQuery):

    length_passwords = str(products[query.data+"_count"])
    await bot.send_invoice(chat_id=query.from_user.id,
                           title=products[query.data][-3],
                           description=str(products[query.data][2]).replace("*", length_passwords), 
                           provider_token=os.getenv("PAYMENT_TOKEN"),
                           photo_url=products[query.data][-1],
                           currency="rub",
                           photo_height=234,     
                           photo_width=416,
                           photo_size=416,
                           is_flexible=False,
                           prices=[ types.LabeledPrice(label=products[query.data][-2], amount=products[query.data][0]) ],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")
            
    

@dp.pre_checkout_query_handler(lambda query: True)
async def echo(pre_check_qu: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_check_qu.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def success_payment(message: types.Message):
    item = SaveData.item
    
    passwords = list(db.return_passwords(item))

    string = ""

    for i in passwords:
        string += f"Network: {i[0]} / <b>{i[1]}</b>\n"
    
    await message.answer(text=string)
    


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)