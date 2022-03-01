from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import os
import json

'''
- Вопросы -
-почему то отдала не всю страницу
-вторая функция криво парсит!!!
'''

'''
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
    
    response = requests.get(url=url, headers=headers)
    # print(response)
    
    # если отсутствует, то создаю директорию
    if not os.path.exists('rbc_news'):
        os.mkdir('rbc_news')
        
    # сохраняю страницу
    with open(file='rbc_news/index.html', mode='w') as file:
        file.write(response.text)
        
    # читаю сохраненую страницу
    with open(file='rbc_news/index.html') as file:
        src = file.read()
        
    soup = BeautifulSoup(markup=src, features='lxml')  
    
    all_news_cards = {}
    
    # нахожу пачку карточек ()
    all_cards = soup.find_all('div', class_='js-index-exclude')
    
    for card_item in all_cards:
        # print(f"{card_item}\n*-*-*-**-*-*-*-***-*-*-*-*-*-*-")
        
        # почему то код видит все карточки, как одну, поэтому яя еще раз перебираю в цикле
        for card in card_item:            
            
            # нахожу title
            # не все карточки с item__title-wrap имеют нужную информацию, поэтому через try
            try:
                card_title = card.find('span', class_='item__title-wrap')
            except Exception as ex:
                # print(ex)
                # print("Не везде, как я хочу!")
                card_title = 'no data'
                
            # пытаюсь обьехать пустые 'item__title-wrap'
            if card_title == 'no data':
                continue
            else:
                card_title_total = card_title.find('span', class_='item__title').text.strip()
                
            # нахожу url карточки
            card_url = card.find ('a', class_='item__link').get('href')
            
            # print(f"{card_title_total}\n{card_url} \n*-*-*-*-*-*-*-*-**-*-*-*-")
            
        # записываю title & url  в словарь
        all_news_cards[card_title_total] = card_url
            
    # print(all_news_cards)
            
    # записываю в json формате словарь all_news_cards
    with open(file='rbc_news/all_news_cards.json', mode='w') as file:
        json.dump(all_news_cards, file, indent=4, ensure_ascii=False)
        
        
'''
функция проверит, есть ли новые посты на странице про криптовалюты
Запишет all_fresh_news_cards.json и старый перезапишет
'''        
def get_data_new(path='rbc_news/all_news_cards_Max.json'):
    
    # сохраняю в переменную словарь с title & url собранный прошлой функцией
    with open(file=path) as file:
        src = json.load(file)
    
    # фэковый  ЮА меняет юзер агента в хэдерсах
    ua = UserAgent()
    url = 'https://www.rbc.ru/crypto/'
    
    headers = {
        'user-agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    
    response = requests.get(url=url, headers=headers)        
    soup = BeautifulSoup(markup=response.text, features='lxml')  
    
    all_fresh_news_cards = {}
    
    # нахожу пачку карточек ()
    all_cards = soup.find_all('div', class_='js-index-exclude')
    
    for card_item in all_cards:
        
        # почему то код видит все карточки, как одну, поэтому я еще раз перебираю в цикле
        for card in card_item:            
            
            # нахожу title
            # не все карточки с item__title-wrap имеют нужную информацию, поэтому через try
            try:
                card_title = card.find('span', class_='item__title-wrap')
            except Exception as ex:
                card_title = 'no data'
                
            # пытаюсь обьехать пустые 'item__title-wrap'
            if card_title == 'no data':
                continue
            else:
                card_title_total = card_title.find('span', class_='item__title').text.strip()
                
            # проверка на присутсвие свежего url в предыдущем словаре
            if card_title_total in src:
                continue
            else:                
                # нахожу url карточки
                card_url = card.find ('a', class_='item__link').get('href')
                
                # записываю в новый словарь
                all_fresh_news_cards[card_title_total] = card_url
                
                # записываю в старый словарь
                src[card_title_total] = card_url
                
    # print(all_fresh_news_cards)
    
    # записываю словари в json
    with open(file='rbc_news/all_news_cards.json', mode='w') as file:
        json.dump(src, file, indent=4, ensure_ascii=False)
        
    with open(file='rbc_news/all_fresh_news_cards.json', mode='w') as file:
        json.dump(all_fresh_news_cards, file, indent=4, ensure_ascii=False)
        
    return all_fresh_news_cards
        
        
# def main():
#     # get_data()
#     get_data_new()
    
    
# if __name__ == '__main__':
#     main()
