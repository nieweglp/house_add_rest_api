from bs4 import BeautifulSoup
from requests import get
from uuid import uuid4


def get_urls(pages=2):
    """Function returns add urls for given number of pages.
    Parameters:
        pages(int): Number of pages to scrape
    Returns:
        add_urls(list): List of urls
    """

    for current_page in range(1, pages):
        main_url = 'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/page-{0}/v1c9073p{0}'.format(current_page)
        page = get(main_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        base_url = 'https://www.gumtree.pl'
        ad_urls = []
        for link in soup.find_all('a', {'class': 'href-link'}, href=True):
            ad_urls.append(base_url + link['href'])
    return ad_urls


def translate_dict_keys(list_of_ad_dicts):
    """Function translate dictionary keys from Polish names to English.
    Parameters:
        list_of_add_dicts(dict): Dict of add attributtes.
    Returns:
        translated_add_dict(dict): Translated dict of add attributtes.
    """

    translated_keys = {'id': 'id', 'Tytuł': 'title', 'Cena': 'prize',
                    'Opis': 'content', 'Data dodania': 'added_date',
                    'Rodzaj nieruchomości': 'real_estate_type',
                    'Liczba pokoi': 'room_number', 'Liczba łazienek': 'baths_number',
                    'Parking': 'parking', 'Wielkość (m2)': 'size',
                    'Lokalizacja': 'location', 'Na sprzedaż przez': 'sold_by'}
    translated_ad_dict = {}
    for key in list_of_ad_dicts.keys():
        if key in translated_keys.keys():
            translated_ad_dict[translated_keys[key]] = list_of_ad_dicts[key]
    return translated_ad_dict

def scrape_add(add_urls):
    """Function scrape advertisements for a given urls.
    Parameters:
        add_urls(list): List of add urls.
    Returns:
        list_of_add_dicts(list): List of add dicts.
    """

    list_of_add_dicts = []
    for url in add_urls:
        page_add = get(url)
        soup_add = BeautifulSoup(page_add.text, 'html.parser', from_encoding='utf-8')
        field_name = ['Data dodania', 'Na sprzedaż przez', 'Rodzaj nieruchomości',
                        'Liczba pokoi', 'Liczba łazienek', 
                        'Parking',  'Wielkość (m2)']

        add_fields_dict = {}
        add_fields_dict['id'] = str(uuid4())
        for field in field_name:
            try:
                field_value = soup_add.find(text=field).findNext('span').contents[0]
                add_fields_dict[field] = field_value
            except:
                continue

        location = soup_add.find_all('div', {'class': 'location'})
        for loc in location:
            location = loc.get_text()

        add_fields_dict['Lokalizacja'] = location

        add_title = soup_add.find('span', class_='myAdTitle').text
        add_fields_dict['Tytuł'] = add_title.replace('\xa0', '')

        price = soup_add.find('span', class_='amount').text
        add_fields_dict['Cena'] = price.replace('\xa0', '')

        content = soup_add.find('div', class_='description').text
        add_fields_dict['Opis'] = content

        translated_add_dict_list = translate_dict_keys(add_fields_dict)
        list_of_add_dicts.append(translated_add_dict_list)

    return list_of_add_dicts