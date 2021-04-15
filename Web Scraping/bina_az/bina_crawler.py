import requests
from bs4 import BeautifulSoup as BS 
from datetime import date, timedelta, datetime
from babel.dates import format_datetime
from pymongo import MongoClient
import telebot
import time
import pytz
import os,sys

#---------------------DB CONNECTOR------------------------
cluster = MongoClient("") # secret key
db = cluster["bina_az"]

BOT_TOKEN = ''' ''' # Token 
bot = telebot.TeleBot( BOT_TOKEN )
#-------------------- INFORMATIONS ----------------------
crawl_info = [ 
    { "url":"https://bina.az/baki/alqi-satqi/evler?page=", "collection_name":"ev_villa", "location":"baki","max_page":5 },
    { "url":"https://bina.az/xirdalan/alqi-satqi/evler?page=", "collection_name":"ev_villa", "location":"xirdalan","max_page":5 },
    { "url":"https://bina.az/sumqayit/alqi-satqi/evler?page=", "collection_name":"ev_villa", "location":"sumqayit","max_page":5 },

    { "url":"https://bina.az/baki/alqi-satqi/torpaq?page=", "collection_name":"torpaq_sahesi", "location":"baki", "max_page":5 },
    { "url":"https://bina.az/xirdalan/alqi-satqi/torpaq?page=", "collection_name":"torpaq_sahesi", "location":"xirdalan","max_page":5 },
    { "url":"https://bina.az/sumqayit/alqi-satqi/torpaq?page=", "collection_name":"torpaq_sahesi", "location":"sumqayit","max_page":5 },

    { "url":"https://bina.az/baki/alqi-satqi/baglar?page=", "collection_name":"baglar", "location":"baki","max_page":5 },
    { "url":"https://bina.az/xirdalan/alqi-satqi/baglar?page=", "collection_name":"baglar", "location":"xirdalan","max_page":5 },
    { "url":"https://bina.az/sumqayit/alqi-satqi/baglar?page=", "collection_name":"baglar", "location":"sumqayit","max_page":5 },

    { "url":"https://bina.az/baki/alqi-satqi/menziller/yeni-tikili?page=", "collection_name":"yeni_tikil", "location":"baki","max_page":5 },
    { "url":"https://bina.az/xirdalan/alqi-satqi/menziller/yeni-tikili?page=", "collection_name":"yeni_tikil", "location":"xirdalan","max_page":5 },
    { "url":"https://bina.az/sumqayit/alqi-satqi/menziller/yeni-tikili?page=", "collection_name":"yeni_tikil", "location":"sumqayit","max_page":5 },

    { "url":"https://bina.az/baki/alqi-satqi/menziller/kohne-tikili?page=", "collection_name":"kohne_tikili", "location":"baki","max_page":5 },
    { "url":"https://bina.az/xirdalan/alqi-satqi/menziller/kohne-tikili?page=", "collection_name":"kohne_tikili", "location":"xirdalan","max_page":5 },
    { "url":"https://bina.az/sumqayit/alqi-satqi/menziller/kohne-tikili?page=", "collection_name":"kohne_tikili", "location":"sumqayit","max_page":5 },

]


errors = []
pass_errors_url = [ "yasayis-kompleksleri" ]

#------------------FUNCTIONS--------------------

def send_message( msg ):
    bot.send_message(  1289363821 , msg, parse_mode="html" )
    
    #Togrul
    try:
        bot.send_message(  945515376 , msg, parse_mode="html" )
    except:
        pass




def datetime_filter( date_s ):
    
    out = date_s
    
    if( "Bugün" in date_s ):
        out = format_datetime( pytz.utc.localize(datetime.utcnow()).astimezone(pytz.timezone("Asia/Baku"))  , format='dd MMMM Y', locale='az').title() 
    elif ( "Dünən" in date_s  ):
        out = format_datetime( (pytz.utc.localize(datetime.utcnow()).astimezone(pytz.timezone("Asia/Baku")) - timedelta(days=1)) , format='dd MMMM Y', locale='az').title()

    return out.strip()


def get_info( link ):
    
    dict_info = {}
    
    req = requests.get( f"https://bina.az{link}" )
    soup = BS( req.text , 'lxml' )
    
    
    price_header = soup.find( "div" , class_ = "price_header" )
    info = soup.find( "div" , class_ = "item_show_content" ).find( "div", class_ = "info" )
    side = soup.find( "div" , class_ = "item_show_content" ).find( "div", class_ = "side" )
    
    dict_info["url"] = f"https://bina.az{link}"
    dict_info["crawl_date"] = format_datetime( pytz.utc.localize(datetime.utcnow()).astimezone(pytz.timezone("Asia/Baku"))  , format='dd MMMM Y HH:mm', locale='az').title()
    
    dict_info['title'] = price_header.find( "div" , class_ = "services-container" ).find( "h1" ).text
    dict_info["price"] = "".join(price_header.find( "span" , class_ = "price-val" ).text.split())
    dict_info["price_currency"] = price_header.find( "span" , class_ = "price-cur" ).text
    
    dict_info['poster'] = info.find("section" , class_ = "contacts").find( "div" , class_ = 'name' ).find( text = True )
    dict_info['poster_type'] = info.find("section" , class_ = "contacts").find( "div" , class_ = 'name' ).find( "span" , class_ = "ownership").text   
    
    dict_info["Ünvan"] = side.find( 'div' , class_ = 'map_address' ).text.replace( "Ünvan:" , '' )
    
    dict_info["description"] = side.find( "article" ).text.strip()
    
    item_info_data = info.find( "div" , class_ = "item_info" ).find_all()
    dict_info[  item_info_data[0].text.split(":",1)[0]  ] =  item_info_data[0].text.split(":",1)[1]
    dict_info[  item_info_data[2].text.split(":",1)[0]  ] =  datetime_filter(item_info_data[2].text.split(":",1)[1])   
    
    
    table_data = side.find( "div" , class_ = "param_info" ).find( "table" , class_ = "parameters" ).find_all("tr") 
    for val in table_data :
        td = val.find_all("td")
        dict_info[ td[0].text ] = td[1].text
        
    if not ( "İpoteka" in [ i.find_all("td")[0].text for i in table_data ] ):
        dict_info['İpoteka'] = "yoxdur"
    
    
    dict_info['locations'] = side.find( 'div', class_ = "badges_block" ).text
    
    
    coordinates = soup.find("div", {"id": "item_map" }) 
    dict_info["longitude"] = coordinates["data-lat"]
    dict_info["latitude"] = coordinates["data-lng"]
    
    dict_info["image_link"] = soup.find( "div" , class_ = "large-photo thumbnail" ).find( "img" )['src']
    
    
    return dict_info


def get_record_id(collection):

    return collection.find_one( { "_id":"record_id" } )["val"]

def write_to_db(collection , data , record_id):

    collection.update_one( { "_id":"record_id" } , { "$set" :{ "val":record_id } } )
    collection.insert_many( data )
    


def crawl_one_page(page, url_gp_game,last_record, data_list, location):

    global record_id


    request = requests.get( url_gp_game + str(page) )
    soup = BS( request.text , 'lxml' )
            
    items_list = soup.select('div[class="items_list"]')[0].find_all( "div" , class_ = "items-i" )
        
    for item in items_list:
        link_to_item = (item.find("a" , class_ = "item_link")['href'])
        try:
            info = get_info( link_to_item )
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()

            if not ( link_to_item.split("/")[1] in pass_errors_url ):
                errors.append( {"Exception":e, "Function":"get_info", "Link": link_to_item , "Line":exc_tb.tb_lineno } )
            continue
        
        if ( info["url"] == last_record["url"]  ) and ( info["title"] == last_record["title"] ):
            return  True

        data = {"_id": record_id, "seher": location }
        data.update( info )
        data_list.append(data)
        record_id += 1
    
    return False

#--------------------MAIN PART---------------

for crawl_dict in crawl_info:
    
    start_time = time.time()

    url_gp_game = crawl_dict["url"]
    collection = db[crawl_dict["collection_name"]]

    try:
        record_id = get_record_id(collection)
    except Exception as e:
        errors.append( {"Exception":e , "collection": crawl_dict["collection_name"], "seher":crawl_dict["location"]  } )
        break

    
    last_record = collection.find({"seher": crawl_dict["location"] }).sort( "_id" , -1 ).limit(1)
    
    try:
        last_record = last_record[0]
    except Exception as e:
        last_record =  collection.find_one({ "_id": record_id-1 })


    data_list = []
    max_page = crawl_dict["max_page"]
    page = 1
    ok = True

    while ( ok ):
        try:
            is_break = crawl_one_page( page, url_gp_game, last_record,data_list, crawl_dict["location"] )
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors.append( { "Exception":e, "Function":"crawl_one_page", "Line":exc_tb.tb_lineno, "seher":crawl_dict["location"] } )
            break
        page += 1
        
        if  ( (page-1) == max_page) or ( is_break ) :
            ok = False
    

    
    

    if data_list:
        a = data_list[-1]["_id"]
        for i in data_list:
            i["_id"] = a
            a-=1
        data_list.reverse()

        try:
            write_to_db(collection,data_list,record_id)
        except Exception as e:
            errors.append( { "Exception":e, "Function":"write_to_db", "seher":crawl_dict["location"] } )



    

#--------- Remove duplicates ------------

coll_names = [  "ev_villa", "torpaq_sahesi" ,"baglar" ,"yeni_tikil" ,"kohne_tikili" ]

for coll_name in coll_names:

    coll = db[ coll_name ]

    cursor = coll.aggregate(
        [
        {"$group": { "_id": { "Elanın nömrəsi": "$Elanın nömrəsi", "title":"$title"  }  ,    "unique_ids": {"$addToSet": "$_id"}, "count": {"$sum": 1} }},
        {"$match": {"count": { "$gte": 2 }}}
        ]
    )
    response = []
    for doc in cursor:
        del doc["unique_ids"][0]
        for id_ in doc["unique_ids"]:
            response.append(id_)
        
    coll.delete_many({"_id": {"$in": response}})
    


send_message( "ok" )


if errors:
    for error in errors:
        temp = "<b>ERROR:</b>\n\n"
        for key,val in error.items():
            temp += f'''<pre language="c++">{key} : {val}</pre>\n\n'''
        
        send_message(  temp  )


send_message( ("-"*60) )










