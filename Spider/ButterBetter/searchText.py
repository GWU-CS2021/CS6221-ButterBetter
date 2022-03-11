import requests
import tools
import json

def search_by_text_to_json(API_KEY, text, out_file, r = None):
    head = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='
    text = text.replace(' ','%20')
    if r:
        radius = '&radius='+ str(r)
    else:
        radius =''
    tail = '&key=' + API_KEY

    url = head + text + radius + tail
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload).text
    f = open(out_file,'w',encoding='utf-8')
    f.write(response)
    f.close()
    #return response

def search_by_token_to_json(API_KEY, token, out_file):
    head = 'https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken='
    tail = '&key=' + API_KEY

    url = head + token + tail
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload).text
    f = open(out_file,'w',encoding='utf-8')
    f.write(response)
    f.close()
    return response



