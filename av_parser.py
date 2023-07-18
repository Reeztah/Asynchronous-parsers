from bs4 import BeautifulSoup
import aiohttp
import asyncio

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/110.0.0.0 YaBrowser/23.3.4.605 Yowser/2.5 Safari/537.36 '
}


async def write_to_file(filename, data):
    try:
        with open(filename, mode='a', encoding='UTF-8') as parser_file:
            parser_file.write('\n'.join(data) + '\n')
    except IOError as e:
        print(f'Ошибка при записи в файл: {e}')


async def get_html(url, page):
    try:
        async with aiohttp.ClientSession() as session:
          params = {'page': page}
          async with session.get(url, headers=headers, params=params) as response:
            if response.status != 200:
              raise ValueError(f"Ошибка при получении страницы: {response.status} {response.reason}")
            html = await response.text()
            print(html)
            return html
    except (aiohttp.ClientError, ValueError) as e:
        print(f"Произошла ошибка при извлечении страницы: {e}")
        return None


async def parse_http(html):
    soup = BeautifulSoup(html, 'html.parser')
    page_button = soup.find('a', {'class': 'button--default', 'role': 'button', 'href': True})
    listings = soup.find_all('div', {'class': 'listing-item'})
    price_byn = soup.find_all('div', 'listing-item__price')
    price_usd = soup.find_all('div', 'listing-item__priceusd')
    price_list_byn = [int(byn.text.encode('ascii', errors='ignore').decode('UTF-8')[:byn.text.index('.')].rstrip('.'))
                      for byn in price_byn]
    price_list_usd = [int(usd.text.encode('ascii', errors='ignore').decode('UTF-8')[:usd.text.index('$')].rstrip('$'))
                      for usd in price_usd]
    for num, (listing, byn, usd) in enumerate(zip(listings, price_list_byn, price_list_usd)):
        title, link, description, location, date = (
            listing.find('h3', {'class': 'listing-item__title'}).text.strip(),
            'https://cars.av.by' + listing.find('a', {'class': 'listing-item__link'}).get('href'),
            listing.find('div', {'class': 'listing-item__message'}),
            listing.find('div', {'class': 'listing-item__location'}).text.strip(),
            listing.find('div', {'class': 'listing-item__date'}).text.strip())

        if description is not None:
            description = description.text.strip()

        data_description = [
            f'\nМодель автомобиля: {title}',
            f'Местонахождение, дата публикации: {location}, {date}',
            f'Ссылка: {link}',
            f'Описание: {description}',
            f'Цена (BYN): {byn}р/~{usd}$'
        ]

        await write_to_file('parser.txt', data_description)

    return soup, page_button


async def main():
    user_url = input("Введите URL: ")
    page = 1

    while True:
        html = await get_html(user_url, page)
        if html is not None:
            soup, page_button = await parse_http(html)
            if page_button is None:
                break
            page += 1
            print(f'Считывается страница №{page}')
            print('Данные успешно записаны в файл parser.txt')
        else:
            break

    print('Работа программы завершена :)')


if __name__ == '__main__':
    asyncio.run(main())
