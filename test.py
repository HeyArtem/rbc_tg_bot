from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import os
import json

'''
Это Макс переписал по своему парсинг, прицельно!

функция собирает новости из раздела про криптовалюты с www.rbc.ru 
'''
def get_data():
    
    # фэковый  ЮА меняет юзер агента в хэдерсах
    ua = UserAgent()
    url = 'https://www.rbc.ru/crypto/'
    
    headers = {
        'user-agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    
    # response = requests.get(url=url, headers=headers)
    # print(response)
    
    # если отсутствует, то создаю директорию
    # if not os.path.exists('rbc_news'):
    #     os.mkdir('rbc_news')
        
    # # сохраняю страницу
    # with open(file='rbc_news/index.html', mode='w') as file:
    #     file.write(response.text)
        
    # читаю сoхраненую страницу
    with open(file='rbc_news/index.html') as file:
        src = file.read()
        
    soup = BeautifulSoup(markup=src, features='lxml')  
    cards = soup.find_all('span', class_='item__title-wrap')
    
    # print(len(cards))
    
    all_news_cards = {}
    for card in cards:
        card_title = card.text.strip().split()
        card_title = ' '.join([c.strip() for c in card_title])
        card_url = card.previous_element.previous_element.get('href')
        
        all_news_cards[card_title] = card_url
        
    with open('rbc_news/all_news_cards_Max.json', 'w') as file:
        json.dump(all_news_cards, file, indent=4, ensure_ascii=False)
        
    return all_news_cards
    

def main():
    get_data()
    
    
if __name__ == '__main__':
    main()
