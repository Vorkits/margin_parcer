import requests
id=4804718
headers={'user_agent'}
r=requests.get("https://kaspi.kz/shop/p/4804718/?c=750000000&ref=rec-goods",).text
print(r)