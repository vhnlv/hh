'''
Суть программы: найти в интернете текст заданной песни и создать лирикс видео
--длительность песни = количество кадров--
 создать нужное количество кадров со строчками

Результат - https://www.youtube.com/watch?v=tS_sQ9ykmDc

'''


import requests
import glob
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import textwrap
import os

font = ImageFont.truetype("C:/Users/arsen/Documents/projects/lyrics/212_Sports.otf", size = 170)    #шрифт
W, H = (1920,1080)  
url_p = 'https://api.textyl.co/api/lyrics?q='                                                       #источник текстов


def imag(text, sec, source_img, title, frames, artist):                                             #создаем кадр
    para = textwrap.wrap(text, width=17)    
    print(para)
    print(f'len of pafa {len(para)}')        
     
    im = Image.new('RGB', (W,H), (255, 255, 255))             # 
    im.paste(ImageEnhance.Brightness(source_img).enhance(0.5), (0,0))                                  
    draw_text = ImageDraw.Draw(im)

    current_h, pad = 600 - 100*len(para), 20                        #определяем высоту в зависимости от количества строк
    for line in para:                                               #line - слово  /// para - строчка
        w, h = draw_text.textsize(line, font=font)                                  
        draw_text.text(                                                 #
            ((W-w)/2,current_h),
            line,
            fill=('#ffffff'),
            font=font
        )  
        current_h += h + pad
        direc = f"lyrics/connect/{artist}-{title}"
        j = 1
        while j<=frames:
            if os.path.isdir(direc):
                im.save(direc+f'/{sec}_{j}.jpg')      # 
                j += 1
            else:
                os.makedirs(direc)
                im.save(direc+f'/{sec}_{j}.jpg')
                j += 1


name = glob.glob('lyrics/song/*')                               #
for song in name:
    artist = song.split('\\')[1].split('.mp3')[0].split('-')[0]
    title  = song.split('\\')[1].split('.mp3')[0].split('-')[1]
    #print(f'artist: {artist}, title: {title}')
    
    thumb = Image.open('lyrics\\images\\' + song.split('\\')[1].split('.mp3')[0]+'.jpg').resize((1920,1080), Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(radius=20)) #блюрим фон
    #print(thumb)
    response = requests.get(url_p+artist+title)         #получаем текст
    #print(len(response.json()))
    try:
        imag(artist+title, 1 , thumb, title, response.json()[0]['seconds'], artist )    #первый кадр
        for i in range(len(response.json())):                                           
            text = response.json()[i]['lyrics']                                         #пара строк текста
            sec = response.json()[i]['seconds']                                         #секунды начала
            try:
                prev = response.json()[i+1]['seconds']
            except Exception as e:
                prev = response.json()[i]['seconds'] + 4
            #print(prev)
            frames = prev - sec
            if not frames<0:
                imag(text, sec, thumb, title, frames, artist)                   
            else:
                imag(text, sec, thumb, title, sec, artist)  
    except Exception as e:
        print(e)
        print('Нет текста для этого трека')
        pass


