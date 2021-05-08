from bs4 import BeautifulSoup
from requests import get
import re
import pandas as pd


LIMIT = 2

cols = ['Data dodania', 'Rodzaj nieruchomości', 'Liczba pokoi',
       'Liczba łazienek', 'Parking', 'Wielkość (m2)', 'Lokalizacja', 'Tytuł',
       'Cena']

df = pd.DataFrame(columns=cols)

def get_urls():
    # if LIMIT == 1:

    for current_page in range(1, LIMIT):
        url = 'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/warszawa/page-{0}/v1c9073l3200008p{0}'.format(current_page)
        page = get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        base_url = 'https://www.gumtree.pl'
        add_urls = []
        for link in soup.find_all('a', {'class': 'href-link'}, href=True):
            add_urls.append(base_url + link['href'])
    return add_urls

def scrape_add(add_urls):
    list_of_add_dicts = []
    for url in add_urls:
        page_add = get(url)
        soup_add = BeautifulSoup(page_add.text, 'html.parser')

        field_name = ['Data dodania', 'Na sprzedaż', 'Rodzaj nieruchomości',
                        'Liczba pokoi', 'Liczba łazienek', 
                        'Parking',  'Wielkość (m2)']

        add_fields_dict = {}
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
        # df_temp = pd.DataFrame(add_fields_dict, index=[0])
        # df = df.append(df_temp, ignore_index=True)
        # df.to_csv('gum_tree_ads.csv', index=False)
        list_of_add_dicts.append(add_fields_dict)
    return list_of_add_dicts

# def main():
#     urls = get_urls()
#     scrape_add(urls)
#     # print(output)

# if __name__ == "__main__":
#     main()
