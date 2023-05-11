import requests

url = "https://chicmi.p.rapidapi.com/calendar_in_city/"

querystring = {"city": "london", "days": "14", "max_results": "5"}

headers = {
	"X-RapidAPI-Key": "d4ba369aa5msh31ba822955b0a7bp1c2147jsn0b48eb6cab4f",
	"X-RapidAPI-Host": "chicmi.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

data = response.json()

events = data["values"]["events"]

for event in events:
    print("Название мероприятия:", event["event_name"])
    print("Постер:", event["event_preview_url"])
    print("Ссылка на более подробную информацию:", event["detail_url"])
    print("Место проведения:", event["location"])
    print()
