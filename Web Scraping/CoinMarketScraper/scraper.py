from pymongo import MongoClient, UpdateOne
import requests
from bs4 import BeautifulSoup as BS
from time import sleep
from datetime import datetime,timedelta
import random
import json


cluster = MongoClient("") # secret key
db = cluster["crypto"]

collection = db["cryptos"]



root_link = "https://coinmarketcap.com/"

fir_pg = requests.get(root_link)
fir_bs = BS(fir_pg.text, "lxml")

max_page = fir_bs.find( class_ = "pagination" ).find_all( "li", class_ = "page" )[-1].text
max_page = int(max_page)
sleep(2)


for page in range(1, max_page+1 ):
    
    
    req = requests.get( root_link + "?page=" + str(page)   )
    soup = BS( req.text, "lxml" )

    t = soup.find( "script", {"id":"__NEXT_DATA__"} )
    data = json.loads( t.string )["props"]["initialState"]["cryptocurrency"]["listingLatest"]["data"]
    tbody = soup.find("table", class_ = "cmc-table cmc-table___11lFC cmc-table-homepage___2_guh").find("tbody").find_all("tr")

    data_list = []
    for item,tr in zip(data,tbody):
        
        name = item["name"]
        
        if ("-" in name) or (len(name)>18) or ( name[0].isdigit() ) or ( name[-1].isdigit() ):
            continue
        
        tds =  tr.find_all("td")
        link = root_link + tds[2].find( "a", class_="cmc-link" )["href"][1:]
        
        info_dict = { "Name" : name , "Name Symbol":item["symbol"], "link": link, "lastUpdated":  item["lastUpdated"],"dateAdded": item["dateAdded"]  }
        

        data_list.append( UpdateOne( {"_id": item["id"] }, { "$set" : info_dict },  upsert = True )  )
        
        
    collection.bulk_write( data_list )
    sleep(random.randint(2,4))
    

print("succes")


