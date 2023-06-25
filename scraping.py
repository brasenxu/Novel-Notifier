import cloudscraper
from bs4 import BeautifulSoup


def scrape_title(url):
    soup = get_soup(url)
    result = soup.find('h3', class_="title")
    return result.text.strip()


def scrape_thumbnail(url):
    soup = get_soup(url)
    result = soup.find('div', class_="book")
    return result.img['src']


def scrape_chapter_title(url):
    soup = get_soup(url)
    result = soup.find('div', class_="item-value")
    return result.a['title']


def scrape_link(url):
    soup = get_soup(url)
    result = soup.find('div', class_="item-value")
    return result.a['href']


def scraper(url):
    soup = get_soup(url)
    result = soup.find('div', class_="item-value")
    return result.a['title'] + "\n" + result.a['href']


def get_soup(url):
    scrape = cloudscraper.create_scraper()
    page = scrape.get(url)
    return BeautifulSoup(page.content, "html.parser")
