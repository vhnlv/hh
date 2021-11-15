from config import TOKEN
from getalbum import enter_url, enn
import telebot
from telebot import types
import glob
import json
answer_how_to = 'Как скачать песни из вк - /acc\nКак скачать песни из плейлиста - /playlist'
answer_acc = 'Отправь мне <b>ссылку</b> на страницу, например vk.com/id136033674\nили <b>никнейм</b>, например vhnlv\nПо умолчанию загрузятся последние 25 песен. Если нужно другое количество, то отправь через пробел число, например vhnlv <b>50</b>\n<b>Важно, аудиозаписи должны быть открыты</b>'
answer_playlist = 'Отправь мне <b>ссылку</b> на плейлист,\nнапример https://vk.com/audios136033674?z=audio_playlist136033674_69167423\nПо умолчанию загрузятся последние 25 песен. Если нужно другое количество, то отправь через пробел число,\nнапример https://vk.com/audios136033674?z=audio_playlist136033674_69167423 <b>50</b>\n<b>Важно, аудиозаписи должны быть открыты</b>'
answer_faq = 'Если бот отвечает <b>Что то не так с ссылкой</b> -- проверь, открыты ли аудиозаписи\nЕсли такой ответ приходит на плейлист, значит этот альбом нельзя скачать. Вы можете добавить все песни из этого альбома к себе и/или создать собственный плейлсит с этими песнями. Тогда Бот скачает их\n\nЕсли Вы добавили в свой плейлист новые песни и хотите скачать их, то просто отправьте ссылку еще раз, Бот загрузит только новые' 
bot = telebot.TeleBot(TOKEN)
url_groub = 'https://t.me/izvkvtg'

markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Как пользоваться?')
item2 = types.KeyboardButton('Статистика')
item3 = types.KeyboardButton('FAQ')
markup_main.add(item1,item2)

@bot.message_handler(commands=['start'])
def welcome(message):
    add_to_db(message.chat.id)
    #keyboard

    bot.send_message(message.chat.id, 'Добро пожаловать {0.first_name}\nПомогу тебе скачать песни из ВК\nОтправь ссылку на плейлист из ВК'.format(message.from_user), reply_markup=markup_main)
    


@bot.message_handler(commands=['acc'])
def acc(message):
    bot.send_message(message.chat.id, answer_acc, disable_web_page_preview=True, parse_mode='html', reply_markup=markup_main)

@bot.message_handler(commands=['playlist'])
def playlist(message):
    bot.send_message(message.chat.id, answer_playlist, disable_web_page_preview=True, parse_mode='html', reply_markup=markup_main)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.chat.type == 'private':
        if not bot.get_chat_member('@izvkvtg', message.chat.id).status == 'left':  #проверка подписки
            if message.text =='Статистика':
                users = len(glob.glob('db/*'))
                file = open(f"db/{message.chat.id}.txt", "a+")
                file.seek(0)
                line_count = 0
                for line in file:
                    if line != "\n":
                        line_count += 1
                file.close()
                bot.send_message(message.chat.id, f'Пользователей у бота: {users}\nВы скачали {line_count} песен')
            elif message.text == 'Как пользоваться?':
                bot.send_message(message.chat.id, answer_how_to, parse_mode='html')
            elif message.text == 'FAQ':
                bot.send_message(message.chat.id, answer_faq, parse_mode='html')
            else:
                test = flal(message.text)
                if type(test) is tuple:
                    if enter_url(test[0], message.from_user.id, test[1]) == 'Неправильная ссылка':
                        bot.send_message(message.chat.id, 'Что то не так с ссылкой')
                    else:
                        bot.send_message(message.chat.id, 'Загрузка завершена')           
                else:
                    if enter_url(message.text, message.from_user.id) == 'Неправильная ссылка':
                        bot.send_message(message.chat.id, 'Что то не так с ссылкой')  
                    else:
                        bot.send_message(message.chat.id, 'Загрузка завершена')
        else:
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton('Подписаться', url=url_groub)
            markup.add(item1)
            bot.send_message(message.chat.id, 'Вы не подписались на канал', reply_markup=markup)



def flal(txt):
    try:
        a = txt.split(' ')[0]
        b = txt.split(' ')[1]
        return a, b
    except IndexError:
        return txt
def add_to_db(chat_id):
    with open(f'db/users.txt', 'a+') as file:
        file.seek(0)
        list = []
        chat_id = str(chat_id) + '\n'
        for item in file.readlines():
            list.append(item)
        if not chat_id in list:
            file.write(f'{chat_id}')
            file.close()


bot.polling(none_stop=True, interval=0)