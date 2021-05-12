from bs4 import BeautifulSoup
from requests import get

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

        list_of_olx_ads.append(current_ad_dict)

    return list_of_olx_ads

def scrape_otodom(otodom_urls):
    pass


def main():
    olx_urls, otodom_urls = get_urls(pages=2)
    olx_ads = scrape_olx(olx_urls)
    print(olx_ads)


if __name__ == "__main__":
    main()


