
# Разработчик: motionrus
#    Описание: Протестировано с плагином "Anki-leo - LinguaLeo dictionary export" для Google Chrome
#              Решает проблему импорта csv, когда изоборажение и звук не подтягиваются
#              Скрипт скачивает файлы по url и кладет их в дирректорию ANKI_CONTENT_PATH
#              Потом преобразует файл CSV_FILE, вместо ссылок будет название скаченного файла
#              Для работы необходимо указать в какой колонке находится url картинки и музыка.
#              После запуска скрипта появится файл рядом с csv файлом, который нужно импортировать в ANKI
import csv
import requests

ANKI_CONTENT_PATH = '/Users/rus/Library/Application Support/Anki2/1-й пользователь/collection.media'
CSV_FILE = '/Users/rus/Downloads/lingualeo-dict-export1.csv'
# Change right column. First column = 0
PICTURE_COLUMN = 2
SOUND_COLUMN = 5


with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    copy_reader = [x for x in spamreader]
    for row in copy_reader:
        picture_url = row[PICTURE_COLUMN]
        sound_url = row[SOUND_COLUMN]
        if picture_url:
            r = requests.get(picture_url)
            if r.status_code == 200:
                picture_name = picture_url.split('/')[-1]
                with open(ANKI_CONTENT_PATH + '/' + picture_name, 'wb') as f:
                    f.write(r.content)
                row[PICTURE_COLUMN] = picture_name
            else:
                row[PICTURE_COLUMN] = ''
        if sound_url:
            r = requests.get(sound_url)
            if r.status_code == 200:
                sound_name = sound_url.split('/')[-1]
                with open(ANKI_CONTENT_PATH + '/' + sound_name, 'wb') as f:
                    f.write(r.content)
                row[SOUND_COLUMN] = sound_name
            else:
                row[PICTURE_COLUMN] = ''
    new_csv_file = '_modify.'.join(CSV_FILE.rsplit('.', maxsplit=1))
    with open(CSV_FILE + '_1', 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in copy_reader:
            spamwriter.writerow(row)
