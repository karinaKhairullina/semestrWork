from django.shortcuts import render
import requests


def fashion_news(request):
    def get_fashion_news():
        api_key = 'a320e3ed494e4c4bb0350617c7c30a27'
        url = f'https://newsapi.org/v2/everything?q=fashion&apiKey={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['articles']
        else:
            return None

    news = get_fashion_news()
    return render(request, 'news.html', {'news': news})

