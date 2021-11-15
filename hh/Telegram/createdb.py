
def check_db(song_id, chat_id):
    if sum(1 for line in open(f'db/{chat_id}.txt')) <= 50:
        with open(f'db/{chat_id}.txt', 'a+') as file:
            file.seek(0)
            list = []
            for item in file.readlines():
                list.append(item)
            if not song_id in list:
                file.write(f'{song_id}')
                return 'ok'
            else:
                return 'exist'
    else:
        return 'limit'


