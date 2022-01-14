from bs4 import BeautifulSoup
from requests import get
import re
import json


def get_urls(pages):
    """  """
    for page in range(1, pages):
        main_url = 'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/?page={0}'.format(page)
        main_page = get(main_url)
        soup = BeautifulSoup(main_page.text, 'html.parser')
        url_olx_list, url_otodom_list = [], []
        for url in soup.find_all('a', {'data-cy':'listing-ad-title'}, href=True):
            temp_link = url['href']
            if temp_link.find('www.otodom.pl') == -1:
                url_olx_list.append(temp_link)
            else:
                url_otodom_list.append(temp_link)
    return url_olx_list, url_otodom_list

def scrape_olx(olx_urls):
    list_of_olx_ads = []
    for url in olx_urls:
        ad_page = get(url)
        ad_soup = BeautifulSoup(ad_page.text, 'html.parser')

        current_ad_dict = {}
        current_ad_dict['title'] = ad_soup.find('h1', {'data-cy': 'ad_title'}).text
        current_ad_dict['prize'] = ad_soup.find('div', {'data-testid': 'ad-price-container'}).text
        current_ad_dict['content'] = ad_soup.find('div', {'data-cy': 'ad_description'}).text

        script = ad_soup.findAll('script', {'id': 'olx-init-config'})[0].string
        data = script.split("window.__PRERENDERED_STATE__= ", 1)[-1]
        data = re.findall(r'(?<=location\\":).*?(?=,\\"urlPath)', data)[0].replace('\\', '')
        data = json.loads(data)
        current_ad_dict['city'] = data['cityName']
        current_ad_dict['voivodeship'] = data['regionName']

        temp_attribiutes = ""
        for element in ad_soup.find_all('ul', {'class': 'css-sfcl1s'}):
            temp_attribiutes += element.get_text() 

        current_ad_dict['owner'] = re.findall(r'\w+(?<=Cena)', temp_attribiutes)[0][:-4]
        current_ad_dict['price_per_square_meter'] = re.findall(r'(?<=:\s).*(?=\szł)', temp_attribiutes)
        current_ad_dict['flat_level'] = re.findall(r'(?<=Poziom:\s)\d+|Parter', temp_attribiutes)
        current_ad_dict['furnitures'] = re.findall(r'(?<=Umeblowane:\s)Tak|Nie', temp_attribiutes)
        current_ad_dict['market'] = re.findall(r'(?<=Rynek:\s)Pierwotny|Wtórny', temp_attribiutes)
        current_ad_dict['building_type'] = re.findall(r'(?<=Rodzaj zabudowy:\s).*(?=Powierzchnia)', temp_attribiutes)
        current_ad_dict['square_meters'] = re.findall(r'(?<=Powierzchnia:\s)\d+', temp_attribiutes)
        current_ad_dict['room_numbers'] = re.findall(r'(?<=Liczba pokoi:\s)\d+', temp_attribiutes)

        for key in current_ad_dict:
            if isinstance(current_ad_dict[key], list):
                current_ad_dict[key] = current_ad_dict[key][0]

        list_of_olx_ads.append(current_ad_dict)

    return list_of_olx_ads

def scrape_otodom(url):
    # list_of_otodom_ads = []
    # for url in otodom_urls:
    ad_page = get(url)
    ad_soup = BeautifulSoup(ad_page.text, 'html.parser')

    current_ad_dict = {}
    current_ad_dict['title'] = ad_soup.find('h1', {'data-cy': 'adPageAdTitle'}).text
    current_ad_dict['prize'] = ad_soup.find('strong', {'aria-label': 'Cena'}).text
    current_ad_dict['prize_per_square_meter'] = ad_soup.find('div', {'aria-label': 'Cena za metr kwadratowy'}).text
    current_ad_dict['content'] = ad_soup.find('div', {'data-cy': 'adPageAdDescription'}).text
    current_ad_dict['location'] = ad_soup.find('a', {'aria-label': 'Adres'}).text

    temp_attribiutes = ""
    for element in ad_soup.find_all('div', {'class': 'css-1d9dws4'}):
        temp_attribiutes += element.get_text()

    # current_ad_dict['owner'] = re.findall(r'\w+(?<=Cena)', temp_attribiutes)[0][:-4]
    current_ad_dict['flat_level'] = re.findall(r'(?<=Piętro:\s)\d+|Parter', temp_attribiutes)
    # current_ad_dict['furnitures'] = re.findall(r'(?<=Umeblowane:\s)Tak|Nie', temp_attribiutes)
    current_ad_dict['market'] = re.findall(r'(?<=Rynek:\s)Pierwotny|Wtórny', temp_attribiutes)
    current_ad_dict['building_type'] = re.findall(r'(?<=Rodzaj zabudowy:\s)\w+', temp_attribiutes)
    current_ad_dict['square_meters'] = re.findall(r'(?<=Powierzchnia:\s)\d+', temp_attribiutes)
    current_ad_dict['room_numbers'] = re.findall(r'(?<=Liczba pokoi:\s)\d+', temp_attribiutes)

    return current_ad_dict


def main():
    # olx_urls, otodom_urls = get_urls(pages=2)
    # olx_ads = scrape_olx(olx_urls)
    otodom_ads = scrape_otodom('https://www.otodom.pl/pl/oferta/bezczynszowe-2-pokojowe-mieszkanie-garaz-piwnica-ID4cS4H.html')
    print(otodom_ads)


if __name__ == "__main__":
    main()


