import time
from playwright.sync_api import sync_playwright
from bs4  import BeautifulSoup
import pandas as pd


userNameOfAccount="elonmusk"   # enter username of account here
Total_scrolls=100   # total number of scrolls you want to do

link="https://twitter.com/"+userNameOfAccount

cont=""  # initializing variable for html content 


'''
To understand this code, kindly first README.MD!
'''

data=[]   # in which our records will be appended

with sync_playwright() as p:
    browser= p.chromium.launch(headless=True)
    page=browser.new_page()
    page.goto(link,timeout=500000)
    
    inital_height=0
    final_height=1000
    for i in range(Total_scrolls):  
        page.mouse.wheel(inital_height,final_height)
        inital_height=final_height
        final_height=final_height+300
        time.sleep(4)
        cont+=page.content()

    browser.close()

soup=BeautifulSoup(cont,'html.parser')

all_posts=soup.find_all('div',{'data-testid':'cellInnerDiv'})
for i in all_posts:

    check_retweet=i.find('div',{'role':'link'})

    if check_retweet==None:

        try:
            tweet=i.find('div',{'data-testid':'tweetText'}).get_text(strip=True)
        except:
            pass
        else:

            comments=i.find('div',{'data-testid':'reply'}).get_text(strip=True)
            likes=i.find('div',{'data-testid':'like'}).get_text(strip=True)
            retweets=i.find('div',{'data-testid':'retweet'}).get_text(strip=True)
    
    data.append({
        'Tweet':tweet,
        'Likes':likes,
        'Comments':comments,
        'Re-tweets':retweets
    }
    )

df=pd.DataFrame(data)
df.drop_duplicates(inplace=True)  # to remove duplicates, our final dataframe will contain dublicates!
df.to_excel('output.xlsx',index=False)
