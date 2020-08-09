import requests


r = requests.get('https://en.wikipedia.org/wiki/Raspberry_Pi')
print(r.text)