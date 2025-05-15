import asyncio

import requests
from aiohttp import ClientSession
from bs4 import BeautifulSoup

CYRILLIC_LOWER = [(lambda c: chr(c))(i) for i in range(1072, 1104)]
CYRILLIC_UPPER = [(lambda c: chr(c))(i) for i in range(1040, 1072)]
CYRILLIC_ANSI = CYRILLIC_LOWER + CYRILLIC_UPPER


def get_links():
    url = 'https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту'

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    container = soup.find('div', class_='ts-module-Индекс_категории-container')

    lists = container.find_all('ul', class_='ts-module-Индекс_категории-multi-items')

    links = []
    for ul in lists:
        for li in ul.find_all('li'):
            a_tag = li.find('a', class_='external text')
            if a_tag and 'href' in a_tag.attrs:
                links.append(a_tag['href'])

    return links


async def parse_website(url, session):
    try:
        async with session.get(url) as response:
            response.raise_for_status()

            html = await response.text()

            soup = BeautifulSoup(html, 'html.parser')

            container = soup.find('div', class_='mw-category mw-category-columns')

            if not container:
                print("Не найден div с классом mw-category mw-category-columns")
                return []

            animals_dict = dict()

            for group in container.find_all('div', class_='mw-category-group'):
                letter = group.find('h3').get_text(strip=True).upper()
                # проверка, тк на последних страницах начинаются животные на английском
                if letter not in CYRILLIC_ANSI:
                    continue

                links = group.select('ul li a')

                animals_names = [a.get_text(strip=True) for a in links if a.get_text(strip=True)]

                if letter in animals_dict:
                    animals_dict[letter].extend(animals_names)
                else:
                    animals_dict[letter] = animals_names

            return animals_dict

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


async def process_urls(urls, batch_size=10):
    animals = []
    async with ClientSession() as session:
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i + batch_size]
            tasks = [parse_website(url, session) for url in batch]
            batch_results = await asyncio.gather(*tasks)

            for result in batch_results:
                animals.append(result)

    return animals


async def main():
    links = get_links()

    animals = await process_urls(links)

    result = {}

    for item in animals:
        for letter, words in item.items():
            if letter in result:
                result[letter].extend(words)
            else:
                result[letter] = words.copy()

    # тк животные с разных страниц могут повторяться
    result = {letter: len(set(word_list)) for letter, word_list in result.items()}

    with open('beasts.csv', 'w', encoding='utf-8') as f:
        for letter in CYRILLIC_UPPER:
            count = result.get(letter, 0)
            f.write(f"{letter},{count}\n")


if __name__ == "__main__":
    asyncio.run(main())
    # тут не придумал какие тесты можно сделать
