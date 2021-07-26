#!/usr/bin/env python3
from os import system
from os.path import exists
import datetime
from csv import DictWriter, DictReader

headers = {
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/83.0.4103.141 Safari/537.36'
}


__version__ = 'v0.1.6'

# Константы логирования
FIELDS_LOG_FILE = ['version', 'date', 'cause', 'status']
FILE_LOG = 'file.log'


def get_articles():
    """ Сбор артикулов в файл """
    file_with_link = 'link.txt'
    file_with_articles = 'articles.txt'
    if exists(file_with_link) is False:
        try:
            write_log('Добавление ссылки', 'Run')
            print('\nСсылка сохранится')
            while True:
                link = input('Введите ссылку WB: ')
                if link == '':
                    print('Поле ввода не должно быть пустым')
                    write_log('Пустое поле для ссылки', 'Fail')
                else:
                    break
            with open(file_with_link, 'a') as file:
                file.write(link)
                file.close()
            write_log('Ссылка добавлена', 'OK')
        except Exception as error_else:
            write_log(error_else, 'Fail')

    if exists(file_with_articles) is False:
        with open(file_with_articles, 'a') as file:
            file.write('')
            file.close()
    else:
        with open(file_with_articles, 'w') as file:
            file.write('')
            file.close()
        write_log('Перезапись артикулов', 'OK')

    url_main = open(file_with_link).readline()
    cnt = 0
    # Инициализация перехода по страницам
    write_log('Сбор данных', 'Run')
    for page_now in range(1, 10):
        mas_articles = []
        page = get_req(url_main)
        soup = BeautifulSoup(page.content, 'html.parser')

        for line in soup.findAll('a', href=True):
            if "detail.aspx?" in line["href"]:
                cnt += 1
                article_url = line['href']
                article_url = article_url[9::]
                article = ''
                for number in article_url:
                    if number == '/':
                        break
                    else:
                        article += number
                mas_articles.append(article)
                # Запись артикулов в файл
                with open(file_with_articles, 'a') as articles_file:
                    articles_file.write(article)
                    articles_file.write('\n')
                system("clear")
                print('Собрано артикулов: ', cnt)
        url_main = url_main.replace("page=" + str(page_now), "page=" + str(page_now + 1))
    if cnt == 0:
        write_log('Артикулы не собраны', 'Fail')
        print('Артикулы не собраны. Возможно, проблема в ссылке')
        quit()
    else:
        write_log('Артикулы собраны', 'OK')
        print('\n Собранные артикулы находятся в', file_with_articles)
        write_log('Успешно', 'OK')
        input("\n\n Нажмите \'Enter\'")


def write_log(cause, status_itself):
    """ Логирование """
    def get_time_now():
        hms = datetime.datetime.today()
        time_format = str(hms.hour) + ':' + str(hms.minute) + ':' + str(hms.second)
        date_format = str(hms.day) + '.' + str(hms.month) + '.' + str(hms.year)
        total = str(time_format) + '-' + str(date_format)
        return ''.join(total)

    if exists(FILE_LOG) is False:
        with open(FILE_LOG, mode="a", encoding='utf-8') as data:
            logs_writer = DictWriter(data, fieldnames=FIELDS_LOG_FILE, delimiter=';')
            logs_writer.writeheader()

    log_data = open(FILE_LOG, mode="a", encoding='utf-8')
    log_writer = DictWriter(log_data, fieldnames=FIELDS_LOG_FILE, delimiter=';')
    log_writer.writerow({
        FIELDS_LOG_FILE[0]: __version__,     # Запись версии
        FIELDS_LOG_FILE[1]: get_time_now(),  # Запись даты и времени
        FIELDS_LOG_FILE[2]: cause,           # Запись причины
        FIELDS_LOG_FILE[3]: status_itself    # Запись статуса
    })


if __name__ == '__main__':
    try:
        from bs4 import BeautifulSoup
        from requests import get as get_req
        from sys import platform as _platform
        write_log('Запуск программы', 'Run')
        get_articles()
        write_log('Работа завершена', 'OK')
    except ModuleNotFoundError as error:
        write_log(error, 'Fail')
        error = str(error)
        print('Установите отсутствующий/отсутствующие модуль/модули', error[15:], 'через PIP')
        print('\n Для установки всех отсутвующих модулей введите команду в терминале:')
        print('pip3 install -r requirements.txt')
    except Exception as error_r:
        write_log(error_r, 'FAIL')
