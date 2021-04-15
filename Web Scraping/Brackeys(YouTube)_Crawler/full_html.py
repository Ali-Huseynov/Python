from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup


# return count of found videos
def get_count_of_videos(html):
    soup = BeautifulSoup(html, 'lxml')

    videos = soup.find_all('ytd-grid-video-renderer', class_='style-scope ytd-grid-renderer') # get all videos of current html

    return len(videos)


# save html file of scrolled to the endo of page
def save_full_html(link , time , height = 3000):

    # use for hide chrome window
    # opt = webdriver.ChromeOptions()
    # opt.add_argument('headless')



    driver = webdriver.Chrome()#options = opt) 

    driver.get(link)

    last_len = get_count_of_videos(driver.page_source) # count of videos of current html
    init_height = height # you also can change height , but initially it is 3000

    while True:
        driver.execute_script("window.scrollTo(0, {})".format(init_height))

        sleep(time) # loading page

        html = driver.page_source # new html
        new_len = get_count_of_videos(html) # count of videos of new html
        if last_len==new_len:
            break
        last_len = new_len
        init_height+=height

    print(last_len) # should be 461

    # save html
    with open('full_html.html' , 'w' , encoding='utf-8') as full_html:
         full_html.write(html)


    driver.close()



if __name__ == '__main__':
    link = 'https://www.youtube.com/c/Brackeys/videos'
    save_full_html(link , 5) # choosing time of sleep is depend of your internet connection(if your connection is poor then set it more than 5)

