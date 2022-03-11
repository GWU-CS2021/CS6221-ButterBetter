import requests

text = 'restaurants nearby GWU'
YOUR_API_KEY = 'AIzaSyC4DMtNlVt4fQrDry1SJU4AtwE6750x61c'

def textProcess(text):
    head = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='
    text = text.replace(' ','%20')
    tail = '&key=' + YOUR_API_KEY
    return head + text + tail

url = textProcess(text)

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)


