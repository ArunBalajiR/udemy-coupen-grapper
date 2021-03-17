
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import json

def scrape_category(name):
    base_url = 'https://udemycoupon.learnviral.com/coupon-category/' + name + '/'
    source = requests.get(base_url).text
    soup = BeautifulSoup(source, 'html.parser')
    contents = soup.find_all('div', class_='item-holder')
    courses = []
    for item in contents:
        heading = item.find('h3', {'class': 'entry-title'}).text.replace('[Free]', '')
        image = item.find('div', {'class': 'store-image'}).find('img')['src']
        course_link = item.find('a', {'class': 'coupon-code-link btn promotion'})['href']
        success_rate = item.find('span', {'class': 'percent'}).text
        courses.append({
            "heading": heading,
            "image": image.replace('240x135', '750x422'),
            "courselink": course_link,
            "successrate" : success_rate,
        })

    return courses


def index(req):
    result = {}
    for category in ("development", "it-software", "business", "office-productivity", "personal-development"," design", "marketing","language", "test-prep"):
        result[category] = scrape_category(category)

    data = json.dumps([result])  # or print([result])
    return render(req, 'index.html', {'courses': data})
def all(req):
    for category in ("development", "it-software", "business", "office-productivity", "personal-development"," design", "marketing","language", "test-prep"):
        data = json.dumps(scrape_category(category))
    return render(req, 'index.html', {'courses': data})

