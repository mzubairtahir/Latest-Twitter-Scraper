import time
from playwright.sync_api import sync_playwright
from bs4  import BeautifulSoup
import pandas as pd

data=[]
link="https://twitter.com/elonmusk"
cont=""
with sync_playwright() as p:
    browser= p.chromium.launch(headless=True)
    page=browser.new_page()
    page.goto(link,timeout=500000)
    
    inital_height=0
    final_height=1000
    for i in range(100):  # 4== 51 
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
df.drop_duplicates(inplace=True)  
df.to_excel('elonfinal.xlsx',index=False)
