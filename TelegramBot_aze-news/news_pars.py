import requests
from bs4 import BeautifulSoup
import sqlite3


def more_info(link):

    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    quiz_holder = soup.find("div" , class_ = "quiz-holder" )

    category = quiz_holder.find( "span" , class_ = "category" ).text
    title = quiz_holder.find( "h1" ).text
    id_by_category = link.split('/')[-1].split('.')[0]

    return title , category , id_by_category

    



def have_news():

    source = requests.get('https://news.milli.az/').text

    soup = BeautifulSoup(source, 'lxml')

    news = soup.find('ul', class_='post-list2').find("li")

    link = news.find( "div" , class_ = "text-holder").find( "strong" ).find("a")["href"]

    title ,category , id_by_category = more_info(link) 

    data = sqlite3.connect("data.db")

    with data:
        command = f"SELECT id FROM News WHERE category = '{category}' and id_by_category = {id_by_category} "
        query = list(data.execute( command ))


    if query:
        print( "Exist\n" )
        return False


    with data:
        command = f" INSERT INTO News(title , category , date_of_publ,id_by_category ) VALUES ( '{title}' , '{category}', datetime('now','localtime') , {id_by_category}  ) " 
        data.execute( command )


    return [category,link]





if __name__ =="__main__":
    have_news()
    




