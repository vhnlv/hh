import collections
import vk_api
from vk_api.audio import VkAudio
import requests
import json
import telebot
import os
from logpass import log
from config import TOKEN
from itertools import islice
#songs_info = [{'id': 456239050, 'owner_id': 364912749, 'track_covers': ['https://sun2-10.userapi.com/impf/c850732/v850732674/25e9/PBNKj1h2G-s.jpg?size=80x80&quality=96&sign=fd69730b0e99280401917f4378e52bf4&type=audio', 'https://sun2-10.userapi.com/impf/c850732/v850732674/25e9/PBNKj1h2G-s.jpg?size=150x150&quality=96&sign=99dacda7c68789ed0b10bc9898bb9c2c&type=audio'], 'url': 'https://cs2-8v4.vkuseraudio.net/p2/d17e56edfe5859.mp3?extra=uJE98xeSLJDc663BOIPduUTuKjb6IcasT48j-XovbT_l5StNboW-vUiPoIp6s8-85iv8SJ2IiZ5Y2HQLwY4lyj8FeaPRy5AWA3Wj9fa9cwl_clVR8ZZ0uvusGLDP4BWZqKXuwMeJKSfNSCuzHPTGwjg4Hg&long_chunk=1', 'artist': '6LACK, Khalid', 'title': 'Seasons', 'duration': 250}, {'id': 456239048, 'owner_id': 364912749, 'track_covers': ['https://sun9-32.userapi.com/impf/c855216/v855216733/2319b5/5x8Y_4J0uT8.jpg?size=80x80&quality=96&sign=7a5120883c035101ed31627cce5e61e2&type=audio', 'https://sun9-32.userapi.com/impf/c855216/v855216733/2319b5/5x8Y_4J0uT8.jpg?size=150x150&quality=96&sign=338b410187bfdec029b7882eaec73fa3&type=audio'], 'url': 'https://cs2-2v4.vkuseraudio.net/p4/e41d2b60f4e694.mp3?extra=2kfoV7CRuUvG_-WfkXrgDaB5OHzfggsZwzEOk0eXqkZeTprFB8tSqoYAIjmyW36exiOyHLm9JCRE1mfu6gvMp8jU7GEBgUv1wPsEM5IcGjPAlWRPRbQBiVGLrfgKLwcRhJcrESiIoEACgDTPTf1Qh1MGtQ&long_chunk=1', 'artist': 'Drake', 'title': 'Now & Forever', 'duration': 281}, {'id': 456239047, 'owner_id': 364912749, 'track_covers': ['https://sun2-4.userapi.com/impf/c855132/v855132457/25b057/qc_N5LGOVCc.jpg?size=80x80&quality=96&sign=6176a711684f7625c759a652a7f09bf7&type=audio', 'https://sun2-4.userapi.com/impf/c855132/v855132457/25b057/qc_N5LGOVCc.jpg?size=150x150&quality=96&sign=c399037e15dd2f62cf2929f6079ef80c&type=audio'], 'url': 'https://cs1-62v4.vkuseraudio.net/p12/7cdc060a8a58dc.mp3?extra=LhDMAVCiX3TyZlBISqzjdRotM8jJS2FBK-wnFrsWW3i1hP1GYceavUSdvojiOE5bWM43uXL5K_-vOgQWXc8JgwYzg9g--nDhB2dLqVNcgbcHgwCKqMzebJ5TLNoXyRHIk98imJBddVWXv5ZVRkZwX3qGBg&long_chunk=1', 'artist': 'Khalid', 'title': '8TEEN', 'duration': 228}, {'id': 456239046, 'owner_id': 364912749, 'track_covers': [], 'url': 'https://cs2-1v4.vkuseraudio.net/p4/a46abfa976fb86.mp3?extra=hBtsOS4OAWYEt1KLvu1fXBhG0sA5TO80QwapolpD96yOifS1DXHyhKZUB7ennmlSPzVfsrpt4Pj7KzWtnJLFSCmI_9l7FJtZxsvmWUj8H5r5HJuAV1yVODgoMI4_G0_xCUCPQCxo6c8FkPZdckQve5vtHA&long_chunk=1', 'artist': 'Lil Peep & Teddy', 'title': 'Dreams x Nightmares', 'duration': 226}, {'id': 456239045, 'owner_id': 364912749, 'track_covers': ['https://sun2-3.userapi.com/impf/c857632/v857632685/23ff37/a0-PdtJCCQw.jpg?size=80x80&quality=96&sign=89d43114d7cdb3e296ad14aa4cb9ca5c&type=audio', 'https://sun2-3.userapi.com/impf/c857632/v857632685/23ff37/a0-PdtJCCQw.jpg?size=150x150&quality=96&sign=710cc83c490c5f6fd4d0844a4cd7a691&type=audio'], 'url': 'https://cs2-8v4.vkuseraudio.net/p1/b1fee70e66dc7c.mp3?extra=acKMjF32AIQ4z7G1_cCBX2s5iGBvQVRPo0he3YO1DmMOAcWU6dqCrx9ORCxs4naLCsrclEi4uwmcKvHR5n0lD7jxv25vfPwA8zbfr-RvW_zwpggMRtSt_tMgMBnrRrhCPJDikSNR35ARGm99VQXoShL51A&long_chunk=1', 'artist': 'DaniLeigh', 'title': 'Last Night', 'duration': 145}, {'id': 456239044, 'owner_id': 364912749, 'track_covers': ['https://sun9-37.userapi.com/impf/n7YUsZ4iQDqf_XfuIoqXRI3akksFQ7FgttEAbA/IHVpLA1WWfI.jpg?size=80x80&quality=96&sign=ebf3add2ea2cd0074ab7aec23e62c5d4&type=audio', 'https://sun9-37.userapi.com/impf/n7YUsZ4iQDqf_XfuIoqXRI3akksFQ7FgttEAbA/IHVpLA1WWfI.jpg?size=150x150&quality=96&sign=9f45ada25a054d337ded78aa38b6b708&type=audio'], 'url': 'https://cs2-1v4.vkuseraudio.net/p1/008e7e72180394.mp3?extra=I_RvpJst4OQWe53SkAORSQUPUCQp92hSJtqvHRgt9BjBKdpG-tW6OF2wqV2pkimgUZB6LSZYbrSsv1GPi-q11KTqPP_h6LQZWp-k1YbaCpM3IqSGGyDJkq0JQO1aalCzSibwRhxOSmeiFifiUMxhIfGyLg&long_chunk=1', 'artist': 'PARTYNEXTDOOR', 'title': 'SHOWING YOU', 'duration': 286}]
#TOKEN = open('tok.txt', 'r').read()                          #токен телеги

bot = telebot.TeleBot(TOKEN)                                 #создан бот

URL_REQUEST = f'https://api.telegram.org/bot{TOKEN}/sendAudio'

vk_session = vk_api.VkApi(log[0], log[1])       
vk_session.auth()
vk = vk_session.get_api()
vkaudio = VkAudio(vk_session)
chat_id = '243207135'
CHAT_ID_TRASH = '-1001452108477'
def_count = '2'
def enter_url(link, chat_id, count=def_count):
    print(link)
    print(count)
    if get_songs_from_pl(link, chat_id, count) == 'Неправильная ссылка':
        return get_songs_from_user(link, chat_id, count)                                                   #
                                                                                                    #
def get_songs_from_pl(link, chat_id, count=def_count):               #качаем треки из плейлиста             <-########
    owner_album = get_playlist(link)                                                                #
    if not owner_album == 'Неправильная ссылка':                                        
        try:
            songs_all = vkaudio.get_iter(owner_id=owner_album[0], album_id=owner_album[1])
            songs_info = next_songs(songs_all, count)
            get_songs(songs_info, chat_id)
            return 'все ок'                         #ПОМЕНЯТЬ
        except Exception:
            return 'Неправильная ссылка'
    else:
        return 'Неправильная ссылка'  

def get_playlist(link):         #извлекаем из ссылки айди и плейлист
    if '?' in link: 
        try:
            owner_id = link.split('playlist')[-1].split('_')[0]
            album_id = link.split('playlist')[-1].split('_')[1].split('/')[0]
            if owner_id.isdigit() and album_id.isdigit():
                return owner_id, album_id
        except Exception:
            return 'Неправильная ссылка'
    else:        
        try:
            owner_id = link.split('/')[-1].split('_')[0]
            album_id = link.split('/')[-1].split('_')[1]
            if owner_id.isdigit() and album_id.isdigit():
                return owner_id, album_id
            else:
                return 'Неправильная ссылка'
        except Exception:
            return 'Неправильная ссылка'

def get_vk_id(screen_name):           #получить айди по шортнейму  
    if screen_name.isdigit():
        return screen_name
    elif '/' in screen_name:
        try:
            return vk.utils.resolveScreenName(screen_name=screen_name.split('/')[-1])['object_id']
        except Exception:
            return 'Неправильная ссылка'
    else:
        try:
            return vk.utils.resolveScreenName(screen_name=screen_name)['object_id']
        except Exception:
            return 'Неправильная ссылка'




def get_songs(songs_info, chat_id):
    url_song = list(map(lambda x: x['url'], songs_info))
    artist = list(map(lambda x: x['artist'], songs_info))
    title = list(map(lambda x: x['title'], songs_info))
    song_id_list = list(map(lambda x: x['id'], songs_info))
    duration_list = list(map(lambda x: x['duration'], songs_info))
    for i in range(len(url_song)):
        url_of_song = url_song[i]
        artist_name = artist[i]
        title_of_song = title[i]
        song_id = song_id_list[i]
        duration = duration_list[i]
        if check_db(song_id, chat_id) == 'ok':
            download_songs(url_of_song, artist_name, title_of_song, chat_id, duration)
        #elif check_db(song_id, chat_id) == 'exist':
         #   return 'Этот трек уже был загружен'
        #else:
         #   return 'Лимит'
      
def check_db(song_id, chat_id):
    print(chat_id)
    print('================CHAT Id')
    song_id = str(song_id) + '\n'
    file_db = open(f'db/{chat_id}.txt', 'a+')
    file_db.close()
    if sum(1 for line in open(f'db/{chat_id}.txt')) <= 50:
        with open(f'db/{chat_id}.txt', 'a+') as file:
            file.seek(0)
            list = []
            for item in file.readlines():
                list.append(item)
            if not song_id in list:
                file.write(f'{song_id}')
                file.close()
                return 'ok'
            else:
                return 'exist'
    else:
        return 'limit'

def download_songs(url_of_song, artist_name, title_of_song, chat_id, duration):
    data = (
        ('chat_id', CHAT_ID_TRASH),
        ('audio', url_of_song),
    )
    response = requests.post(URL_REQUEST, data=data)            #отправялю трек в помойку
    
    
    print(response.text)
    file_id = json.loads(response.text)['result']['audio']['file_id']   #извлекаю из помойки
    path = bot.get_file(file_id)
    file = path.file_path
    print(path)
    print(file)
    download = bot.download_file(file) 
    #print(download)
    #bot.send_document()                                 #качаю и отправляю пользователю
    print(bot.send_audio(chat_id=chat_id, audio=download, performer=artist_name, title=title_of_song, duration=duration))
    print(response)


def get_songs_from_user(link, chat_id, count=def_count):                      #качаем треки у пользователя
    vk_id = get_vk_id(link)
    if not vk_id == 'Неправильная ссылка':
        try:
            songs_all = vkaudio.get_iter(owner_id=vk_id)
            songs_info = next_songs(songs_all, count)
            print(songs_info)
            get_songs(songs_info, chat_id)
            return 'все ок'                         #ПОМЕНЯТЬ
        except Exception:
            return 'Неправильная ссылка'
    else:
        return 'Неправильная ссылка'  

def enn(link, chat_id):
    print(link)
    print(chat_id)


#songs_info = vkaudio.get_iter(owner_id='136033674')

def next_songs(songs_all, count=def_count):
    return list(next(songs_all) for _ in range(int(count)))

#test = flal(text)

#print(test[0])
#print(test[1])
#print(enter_url(test[0], chat_id, test[1]))
#if type(test) is tuple:
 #   print(enter_url(test[0], chat_id, test[1]))
#else:
 #   print(enter_url(text, chat_id))


#print(next_songs(songs_info))
#print(list(next(songs_info) for _ in range(2)))
#print(list(next(songs_info) for _ in range(2)))

#print(get_vk_id('ilavash'))

#print(enter_url('https://vk.com/audios136033674?z=audio_playlist136033674_69167813', chat_id))
#print(get_playlist('https://vk.com/music/playlist/136033674_69167813%4324'))
#print(get_songs(songs_info))

#print(get_playlist('https://vk.com/audio?z=audio_playlist136033674_69167813'))

#print(enter_url('https://vk.com/music/playlist/136033674_69167813_e863320ec6b9d21426'))
#print(enter_url('fiqbeobfuqyouyuyfywbhjwbfhjajeqq'))
#print(get_songs_from_user(link='ilvvash', chat_id='243207135'))
