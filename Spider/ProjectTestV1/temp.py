import requests
import tools

TEXT = 'restaurants nearby GWU'
YOUR_API_KEY = 'AIzaSyC4DMtNlVt4fQrDry1SJU4AtwE6750x61c'
FILE = './Result.json'

def textProcess(text):
    head = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='
    text = text.replace(' ','%20')
    tail = '&key=' + YOUR_API_KEY
    return head + text + tail

url = textProcess(TEXT)

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)
tools.jsonWrite(FILE,response.text)
tools.jsonFileProcess(FILE,'./ProResult.json')

