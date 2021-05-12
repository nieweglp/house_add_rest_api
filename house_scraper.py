from bs4 import BeautifulSoup
from requests import get
import re
import pandas as pd
from uuid import uuid4


def get_urls(pages):
    for current_page in range(1, pages):
        url = 'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/warszawa/page-{0}/v1c9073l3200008p{0}'.format(current_page)
        page = get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        base_url = 'https://www.gumtree.pl'
        add_urls = []
        for link in soup.find_all('a', {'class': 'href-link'}, href=True):
            add_urls.append(base_url + link['href'])
    return add_urls

def scrape_add(add_urls):
    translated_keys = {'id': 'id', 'Tytuł': 'title', 'Cena': 'prize',
                        'Opis': 'content', 'Data dodania': 'added_date',
                        'Rodzaj nieruchomości': 'real_estate_type',
                        'Liczba pokoi': 'room_number', 'Liczba łazienek': 'baths_number',
                        'Parking': 'parking', 'Wielkość (m2)': 'size',
                        'Lokalizacja': 'location'}
    list_of_add_dicts = []
    for url in add_urls:
        page_add = get(url)
        soup_add = BeautifulSoup(page_add.text, 'html.parser')

        field_name = ['Data dodania', 'Na sprzedaż', 'Rodzaj nieruchomości',
                        'Liczba pokoi', 'Liczba łazienek', 
                        'Parking',  'Wielkość (m2)']

        add_fields_dict = {}
        add_fields_dict['id'] = str(uuid4())
        # for field in field_name:
        #     try:
        #         field_value = soup_add.find(text=field).findNext('span').contents[0]
        #         add_fields_dict[field] = field_value
        #     except:
        #         continue

        # location = soup_add.find_all('div', {'class': 'location'})
        # for loc in location:
        #     location = loc.get_text()

        # add_fields_dict['Lokalizacja'] = location

        add_title = soup_add.find('span', class_='myAdTitle').text
        add_fields_dict['Tytuł'] = add_title.replace('\xa0', '')

        # price = soup_add.find('span', class_='amount').text
        # add_fields_dict['Cena'] = price.replace('\xa0', '')

        # content = soup_add.find('div', class_='description').text
        # add_fields_dict['Opis'] = content

        translated_add_dict = {}
        for key in add_fields_dict.keys():
            if key in translated_keys.keys():
                translated_add_dict[translated_keys[key]] = add_fields_dict[key]
            
        list_of_add_dicts.append(translated_add_dict)


    return list_of_add_dicts