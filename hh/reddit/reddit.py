'''
Суть программы: Загрузить лучшие мемы за последние 24 часа с реддита в группу вк.
Использовать метод отложенных записей. 1 мем каждые 30 минут


Результат: https://vk.com/rmeme
'''

import praw
import requests
import json
import io
import datetime
import time
from os import remove
limit = 28
now = datetime.datetime.today()
ti = (now - datetime.datetime(1970,1,1)).total_seconds()  
user_token = "*******************************************************************"

group_id_memes = '202230766'
group_id_2m4m = '202242268'
group_id_night_memes = '201439302'
v = '5.131'


reddit = praw.Reddit(
    client_id='***********',
    client_secret='*******-Lmv4YiPErGVg',
    username='ilavash',
    password='*********',
    user_agent='********'
)

sub_memes = reddit.subreddit('memes')
sub_2m4m = reddit.subreddit('2meirl4meirl')
sub_dunk = reddit.subreddit('dankmemes')

def down_from_any_sub(subr, group_id):                      #достать ссылки на мемы
    memes_hot = subr.top(limit=limit, time_filter='day')    #раздел "горячее"
    i = 0
    stepTime = -9000
    for submission in memes_hot:                            #не брать закрепленные            
        if not submission.stickied:
            urla = submission.url                           #полная ссылка
            name = str(urla).split('.')[-2].split('/')[-1]  #имя файла
            form = str(urla).split('.')[-1]                 #form = формат
            if form == 'jpg' or form == 'png':              #не брать ничего кроме изображений 
                start_time = time.time()
                i += 1
                title = submission.title                    
                if title == '2meirl4meirl':                 
                    title = ' '
                response = requests.get(urla)
                img_path = f'c:/Users/arsen/Documents/projects/vk_photos-master/reddit/{name}.{form}'   #путь для фото
                file = open(img_path, 'wb')                                                             
                file.write(response.content)                                                                    
                file.close()
                file = open(img_path, 'rb')
                send = {'file1': file}
                vkpost(send, stepTime, title, group_id)                                                 #отправить в вк
                file.close()
                stepTime += 1800
                finish_time = time.time()
                print(f'Пост номер {i} был загружен за {finish_time-start_time} сек')
                remove(img_path)                                                                        #удалить с компа мем

def vkpost(file, stepTime, title, group_id):        #опубликовать!
    params = (
        ('group_id', group_id), 
        ('access_token', user_token),        #тут я узнаю сервер куда загружать фотки
        ('v', v),     
    )
    response = requests.post('https://api.vk.com/method/photos.getWallUploadServer', data=params)
    upload_server = json.loads(response.text)['response']['upload_url']  #извлекаю ссылку куда отправлять файлы
    response = requests.post(upload_server, files=file)   
    img_hash = json.loads(response.text)['hash']
    photo = json.loads(response.text)['photo']              #извлекаю параметры для сейвфото
    server = json.loads(response.text)['server']
    params = (
        ('group_id', group_id),
        ('photo', photo),  
        ('server', server),
        ('hash', img_hash),            
        ('access_token', user_token),
        ('v', v),
    )
    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto', data=params)    
    image_id = json.loads(response.text)['response']
    id_list = list(map(lambda x: x['id'], image_id))
    final_photo = 'photo136033674_%s' %id_list[0]
    stepTime += ti                          #ti = time right now
    params = (
        ('from_group', '1'),
        ('owner_id', '-' + group_id),
        ('attachments', final_photo),
        ('access_token', user_token),
        ('publish_date', stepTime),
        ('message', title),
        ('v', v),
    )  
    response = requests.post('https://api.vk.com/method/wall.post', data=params)

down_from_any_sub(sub_dunk, group_id_memes)
down_from_any_sub(sub_2m4m, group_id_2m4m)
