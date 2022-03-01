from aiogram import Bot, Dispatcher, executor, types
import asyncio
import aioschedule
from main import get_data_new
from aiogram.utils.markdown import hlink

'''
Бот должен использовать библиотеку
aioshedule
'''
bot = Bot(token='5129945325:AAEQFdCvUjoqKpDz2P5ifdjuA5w44bO22wc', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# тестовая функция
async def trial_trip():
    name = 'Hello from Semen Semenovich! '
    await bot.send_message(564764469, name, disable_notification=True)
    

# функция должна отправлять новые посты с сайта rbc
async def sending_messages(path=get_data_new()):
    print('function called')
    fresh_news_dict = path
    
    # проверка, что словарь не пустой НЕ РАБОТАЕТ!!
    if len(fresh_news_dict) > 0:
        
        # если в словаре есть новости (это значит, что есть новые новости), то я прохожу по ним в цикле и отправляю в телегу
        for k, v, in fresh_news_dict.items():
            # finished_message = f"{k}: {v}"
            finished_message = f"{hlink(k,v)}"
            await bot.send_message(564764469, finished_message, disable_notification=True)
            
    # если новостей нет, переходим в эту ветку
    else:
        await bot.send_message(564764469, 'Tishina! Nichego Neponatno!', disable_notification=True)
    
    
async def schediler():
    aioschedule.every(30).seconds.do(trial_trip)
    # aioschedule.every(30).seconds.do(sending_messages)
    aioschedule.every().day.at("01:02").do(sending_messages)
    await asyncio.sleep(5)
    
    while True:
        await aioschedule.run_pending()
        
        
async def on_startup(_):
    asyncio.create_task(schediler())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
