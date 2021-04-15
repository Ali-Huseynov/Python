import requests
from bs4 import BeautifulSoup
import os
from  bs4 import Comment
from time import sleep
import pandas as pd


def get_partic_table(comp_soup):

    winner =  [v['href'] for v in comp_soup.find_all('a',{'title':'Ümumi əməliyyatlar'})]
    
    comments = comp_soup.find_all(string=lambda text: isinstance(text, Comment))

    data = ''.join([i.extract() for i in comments])

    soup = BeautifulSoup(data, 'lxml')

    table = soup.find_all('a', {'title': 'Ümumi əməliyyatlar'}, limit=15-len(winner))

    out_links =  winner + [v['href'] for v in table]


    return out_links



def get_comp_data(soup):

    cell = soup.find('div',class_='v2_content ed_row').find('div',class_='ed_row clearfix').find_all('div',class_ = 'col-lg-4 col-lg-offset-1 col-md-4 col-md-offset-1 col-sm-4 col-sm-offset-1 col-xs-12')

    comp_num = cell[0].find('div',class_ = 'contest_info_info_all').find('div').find_all('span')[-1]

    comp_date = [   i.find_all('span')[1].text   for i in cell[1].find('div',class_ = 'contest_info_info_all').find_all('div')[:2]]

    return comp_num.text , ' --- '.join(comp_date)


def extract_table(link):
    html = requests.get(link).text

    soup = BeautifulSoup(html,'lxml')
    try:
        name = soup.find('tbody').find('td',{'align':'right'}).text.replace('Name:','')
    except:
        return None

    title = [ v.text for v in  soup.find('tbody').find('tr',{'align':'center'}).find_all('td')[1:]  ]

    data = {}
    price_num = 1
    for n,k in enumerate(title):
        if k =='Price':
            val = k+str(price_num)
            price_num+=1
        else:
            val=k

        data[val] = [  v.find_all('td')[n+1].text for v in soup.find('tbody').find_all('tr',{'align':'right'})  ]

    out = {'Participant Name':[name]*len(data['Ticket'])}
    out.update(data)

    return out
    







data = {
    'Competition':[],
    'Date':[],
}



comp = requests.get('https://www.investaz.az/forex-yarismasi/statistikalar/').text

soup = BeautifulSoup(comp , 'lxml')

comp_num, date = 'statistika' , 'bilinmir'

#print(comp_num)

user_links = get_partic_table(soup)


len_data = 0
for n,i in enumerate(user_links):
    user_data = extract_table(i)
    if user_data ==None:
            continue

    len_data += len(user_data['Ticket'])

    place = {'Place': [(str(n+1))]*len(user_data['Ticket']) }


    place.update(user_data)


    for i in place:
        try:
            data[i] += place[i]
        except:
            data[i] = place[i]


data['Competition'] += [comp_num] * len_data
data['Date'] += [date] * len_data








df = pd.DataFrame(data)

df.to_excel('result.xlsx', index=False , encoding='utf-8' )

