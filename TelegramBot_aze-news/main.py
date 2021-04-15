from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
import asyncio
import news_pars
from SQL_bot import SQL_bot
import time
import keyboards as kb


# set bot token and admin id
BOT_TOKEN = "" # Token here
admin_id = 1289363821

# open DB to import all users id
data= SQL_bot()
users_id = data.get_subscriptions()
data.close()

# creating bot and dispatcher objects
bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


#  notificate admin by some messages
async def send_to_admin( text , arg = None):
    await bot.send_message(chat_id=admin_id, text=text)



#  \subscribe command
@dp.message_handler(commands=['subscribe'])
async def subscribe(message : Message):
    data = SQL_bot()
    # check if user subscribed
    if data.user_subscribed(message.from_user.id ) == True :
        await message.answer('Siz onsuzda artiq Abunə olubsuz')
    else:
        # add user into db(or change status if user was exist earlier) and add user into user_id list
        data.subscribe(message.from_user.id)
        await new_users(message.from_user.id)
        await message.answer('Siz ugurla Abunə oldunuz')
    data.close()



# \unsubscribe command
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message : Message):
    data = SQL_bot()
    # check if user not subscribed or if user not exist at all
    if data.user_subscribed(message.from_user.id) == False or data.user_exist_id(message.from_user.id)==False:
        await message.answer('Siz onsuzda Abunə deyilsiz')
    else:
        # change user status to 0 in DB and remove from user_id list
        data.subscribe(message.from_user.id , un = True)
        await new_users(message.from_user.id,un=True)
        await message.answer('Siz ugurla Abunədən imtina etdiniz')

    data.close()

# \category command for sending subscribed categories
@dp.message_handler( commands = ['category'] )
async def category(message : Message ):
    text = 'Sizin Abune Oldugunuz Kategoriyalar:\n'
    for name in kb.get_categories( message.from_user.id ):
        text += name+"\n"

    await message.answer(text , reply_markup= kb.greet_kb )



# category handler and redirect to rule
@dp.message_handler()
async def category_handler(message: Message):
    user_id = message.from_user.id
    message_text = message.text
    data = SQL_bot()

    # check if message is category and if user is subscribed
    if (message_text in kb.categories) and (data.user_subscribed(user_id)) :
        #check if it is already subscribed category ( remove category )
        if kb.is_subscribed_category(user_id,message_text) :
            kb.remove_user_category(user_id,message_text)
            await message.answer( text= f"'{message_text}' kategoriyasindan imtina etdininz " )
        else: # add into db
            kb.insert_user_category(user_id , message_text)
            await message.answer( text= f"'{message_text}' kategoriyasina abune oldunuz " )
    else:
        await rule( message )

    data.close()


# in other cases(types) of messages and on strart
@dp.message_handler( commands = ['start'] )
async def rule(message: Message):
    rules = 'Abunə olmaq ücün /subscribe \nAbunədən imtina ücün /unsubscribe \nKategoriya Abunə olmaq ücün /category '
    await message.answer(text=rules)
    # send message to admin which user sended to bot
    if not message.from_user.id == admin_id:
        text = 'user {} with id {} \nsend to your bot:\n\n {}'.format(message.from_user.first_name ,message.from_user.id , message.text )
        await send_to_admin(text=text)

    



# uses while adding/removing users in a users_id list
async def new_users(man_id , un =False):
    global users_id
    if un:
        users_id.remove(man_id)
    else:
        users_id.append(man_id)


# runnig for sending posts to users
async def shedule():

    print("Checking...")    
    # check if there new posts
    news = news_pars.have_news()
    # if exist new posts then send it to all users(by category)
    if news:
        category,link = news
        for id_ in users_id:
            if kb.is_subscribed_category(id_ , category):
                await bot.send_message(chat_id=id_ , text= f"{category}\n{link}" )


# for timimg schedule
def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)


if __name__ == '__main__':

    DELAY = 60
    loop = asyncio.get_event_loop()
    loop.call_later(DELAY, repeat, shedule , loop)
    
    executor.start_polling(dp, on_startup=  lambda i: send_to_admin(text='Bot Started' , arg=i) )
    
