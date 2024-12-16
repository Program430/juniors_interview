import requests
from bs4 import BeautifulSoup
from typing import List
import aiohttp
import asyncio

class BadRequest(Exception): pass


class Parser:
    def __init__(self, start_page, max_connections) -> None:
        self.start_page = start_page
        self.semaphore = asyncio.Semaphore(max_connections)

    def start(self):
        print('Получение ссылок')
        urls = self.get_all_pages_urls()
        print('Обработка ссылок')
        result = asyncio.run(self.get_words_count(urls))
        return result

    def get_all_pages_urls(self):
        response = requests.get(self.start_page)

        if response.status_code != 200:
            raise BadRequest

        soup = BeautifulSoup(response.text, 'html.parser')

        box = soup.find(class_='ts-module-Индекс_категории-container')

        elements = box.find_all(class_='external text')

        if not elements:
            raise 

        links = []
        for i in elements:
            if i.find('b'):
                continue

            text = i.get_text()

            if len(text) == 2:
                url = i.get('href')
                links.append(url)

        print(links)

        links.pop()

        return links

    async def get_words_from_page(self, session, url):
        async with self.semaphore:
            async with session.get(url) as response:
                if response.status != 200:
                    raise BadRequest
                html = await response.text()

        soup = BeautifulSoup(html, 'html.parser')

        box_1 = soup.find(id='mw-pages')

        box_2 = box_1.find(class_='mw-category-group')

        elements = box_2.find_all('a')

        if not elements:
            raise 

        # В ТЗ написано считывать список (Можно было просто посчитать количество)
        words = []
        for i in elements:
            words.append(i.get_text())

        return words

    async def get_words_count(self, urls):
        async with aiohttp.ClientSession() as session:
            words_lists = await asyncio.gather(*[self.get_words_from_page(session, i) for i in urls])

        result = {}
        for i in words_lists:
            first_letter_all_words = i[0][0].upper()
            if first_letter_all_words in result:
                result[first_letter_all_words] += len(i)
            else:
                result[first_letter_all_words] = len(i)
               
        return result


class DataBase:
    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, elements):
        try:
            with open(self.file_name, 'w', encoding='UTF-8') as file:
                for key, value in elements.items():
                    file.write(f'{key},{value}\n')
        except Exception as e:
            print(f'Произошла ошибка при записи в файл: {e}')


parser = Parser(
    'https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from=%D0%90%D0%B2',
    50
)

data_base = DataBase('result.txt')

if __name__ == '__main__':
    words = parser.start()
    data_base.write(words)
