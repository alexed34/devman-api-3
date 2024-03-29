import requests
import os
from dotenv import load_dotenv
import argparse



def shorten_link(token, url):
    link = 'https://api-ssl.bitly.com/v4/bitlinks'
    token = f'Bearer {token}'
    headers = {"Authorization": token}
    if url.startswith('https'):
        url.replace('https', 'http')
    elif url.startswith('http'):
        url
    else:
        url = f'http://{url}'
    response = requests.post(link, headers=headers, json={"long_url": url})
    response.raise_for_status()
    bitilink = response.json()
    return bitilink['id']


def count_clicks(token, bitlink):
    token = f'Bearer {token}'
    headers = {"Authorization": token}
    payload = {'unit': 'day', 'units': '-1'}
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary', params=payload,
                            headers=headers)
    response.raise_for_status()
    click = response.json()
    return click['total_clicks']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='Ваше имя')
    args = parser.parse_args()

    user_input = args.name  
    token_bit = os.getenv('TOKEN_BIT')
    try:
        if user_input.startswith('bit.ly'):
            print('Количество переходов по ссылке битли: ', count_clicks(token_bit, user_input))
        else:
            print('{}{}'.format('http://', shorten_link(token_bit, user_input)))
    except requests.exceptions.HTTPError:
        print('отсутствует страница, код HTTPError')
    except requests.exceptions.ConnectionError:
        print('несуществующий сайт, код ConnectionError ')
    except:
        print('неизвестная ошибка')


if __name__ == "__main__":
    load_dotenv()
    main()
