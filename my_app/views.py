from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from .models import Search
import requests

# Create your views here.
base_url = "https://newyork.craigslist.org/search/sss?query="


def home(request):
    return render(request, 'index.html')


def new_search(request):
    search = request.POST.get('search')
    Search.objects.create(search=search)
    response = requests.get(base_url + quote_plus(search))
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    posts = soup.find_all('li', {'class': 'result-row'})
    post_list = []
    for post in posts:
        price = post.find(class_='result-price').text
        title = post.find(class_='result-title').text
        url = post.find('a').get('href')
        if post.find(class_='result-image gallery'):
            image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            image_url = f'https://images.craigslist.org/{image_id}_300x300.jpg'
        else:
            image_url="https://bitsofco.de/content/images/2018/12/broken-1.png"
        post_list.append((title, price, url,image_url))

    stuff_for_frontend = {'search': search,
                          'posts':post_list}
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
