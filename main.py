#!/usr/bin/env python3
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.114 Safari/537.36'
}


__version__ = 'v0.1.2'


def get_articles():
    file_with_link = 'link.txt'
    file_with_articles = 'articles.txt'

    if exists(file_with_articles) is False:
        with open(file_with_articles, 'a') as file:
            file.write('')
            file.close()
    else:
        with open(file_with_articles, 'w') as file:
            file.write('')
            file.close()

    url_main = open(file_with_link).readline()
    s = 0

    for page_now in range(1, 5):
        mas_articles = []
        page = get_req(url_main)
        soup = BeautifulSoup(page.content, 'html.parser')

        for line in soup.findAll('a', href=True):
            if "detail.aspx?" in line["href"]:
                s += 1
                article_url = line['href']
                article_url = article_url[9::]
                article = ''
                for number in article_url:
                    if number == '/':
                        break
                    else:
                        article += number
                mas_articles.append(article)
                with open(file_with_articles, 'a') as articles_file:
                    articles_file.write(article)
                    articles_file.write('\n')
                if _platform == "darwin":
                    system("clear && printf '\e[3J'")
                elif _platform == 'linux':
                    system('clear')
                print('Собрано артикулов: ', s)
        url_main = url_main.replace("page=" + str(page_now), "page=" + str(page_now + 1))
    input("\n\n Press \'Enter\'")


if __name__ == '__main__':
    try:
        from bs4 import BeautifulSoup
        from requests import get as get_req
        from os import system
        from os.path import exists
        from sys import platform as _platform
        get_articles()
    except ModuleNotFoundError as error:
        error = str(error)
        print('Установите отсутствующий модуль', error[15:], 'через PIP')
        print('Для этого нужно ввести команду в терминале:')
        print('\n python -m pip install -r requirements.txt')
