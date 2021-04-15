from aiogram.types import ReplyKeyboardMarkup
import sqlite3

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)

db = sqlite3.connect("data.db")

with db:
    categories = [ i[0] for i in (db.execute( "SELECT DISTINCT CATEGORY FROM NEWS ORDER BY CATEGORY " ))]


for ind , name in enumerate(categories):
    greet_kb.insert( name )
    if (ind+1) % 3 ==0:
        greet_kb.row()




def get_categories( user_id ):
    with db:
        data = [ i[0] for i in db.execute( f" SELECT DISTINCT CATEGORY_NAME FROM CATEGORY WHERE USER_ID = {user_id} " )]
    return data

def is_subscribed_category(user_id , category):
    with db:
        data = list(db.execute( f" SELECT CATEGORY_NAME FROM CATEGORY WHERE USER_ID = {user_id} AND CATEGORY_NAME = '{category}' "))

    if data: return True
    return False

def insert_user_category(user_id , category):
    with db:
        db.execute( f" INSERT INTO CATEGORY VALUES( '{category}' , {user_id} ) " )

def remove_user_category( user_id , category ):
    with db:
        db.execute( f" DELETE FROM CATEGORY WHERE CATEGORY_NAME = '{category}' AND USER_ID = {user_id}; " )
    