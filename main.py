# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import requests
import os
from time import sleep


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.114 Safari/537.36'
}


__version__ = 'v0.1.0'


def get_articles():
    file_with_link = 'link.txt'
    file_with_articles = 'articles.txt'

    if os.path.exists(file_with_articles) is False:
        with open(file_with_articles, 'a') as file:
            file.write('')
            file.close()
    else:
        with open(file_with_articles, 'w') as file:
            file.write('')
            file.close()

    url_main = open(file_with_link).readline()
    s = progress = 0
    cnt_page = 1
    for page_now in range(10):
        page = requests.get(url_main)
        soup = BeautifulSoup(page.content, 'html.parser')
        for line in soup.findAll('a', href=True):
            if "detail.aspx?" in line["href"]:
                progress += 1
                if progress % 100 == 0:
                    url_main = url_main.replace("page=" + str(cnt_page), "page=" + str(cnt_page + 1))
                    cnt_page += 1

        for line in soup.findAll('a', href=True):
            if "detail.aspx?" in line["href"]:
                if progress > 0:
                    s += 1
                    article_url = line['href']
                    article_url = article_url[9::]
                    article = ''
                    for number in article_url:
                        if number == '/':
                            break
                        else:
                            article += number
                    print(str(s) + ':', article)
                    with open(file_with_articles, 'a') as articles_file:
                        articles_file.write(article)
                        articles_file.write('\n')
                    print((s * 100) // progress, '%')
                    if s % 100 == 0:
                        url_main = url_main.replace("page=" + str(cnt_page), "page=" + str(cnt_page + 1))
                        cnt_page += 1
                else:
                    print('Нет данных для сбора')
    # input('\n\n OK')


if __name__ == '__main__':
    get_articles()
