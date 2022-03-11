import populartimes
import tools
import requests

#function text_process
def text_process(text):
    head = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='
    text = text.replace(' ','%20')
    tail1 = '&radius=500'
    tail0 = '&key=' + YOUR_API_KEY
    return head + text + tail1 + tail0

#Parameters
#Google API KEY
YOUR_API_KEY = 'AIzaSyC4DMtNlVt4fQrDry1SJU4AtwE6750x61c'
#Type of searching ([str] example: [restaurant])
search_type = "restaurant"
#Test current location as GWU in Google Map (38.899793, -77.048584)
current_lat = 38.899793
current_lng = -77.048584
#Set param for bound
bound_lower_lat = current_lat-0.00025
bound_lower_lng = current_lng-0.001
bound_upper_lat = current_lat+0.00025
bound_upper_lng = current_lng+0.001
#Set radius
radius = 5000
#text
text = 'restaurants nearby George Washington University, DC'
#text search URL
url = text_process(text)
#response setting
payload={}
headers = {}
#get textsearch response
text_response = requests.request("GET", url, headers=headers, data=payload)

'''
Result = populartimes.get_id(YOUR_API_KEY, "ChIJSYuuSx9awokRyrrOFTGg0GY")

ResultTxt = open('resultGetid.json', 'w')

ResultJS = json.dumps(Result)
ResultTxt.write(ResultJS)

ResultTxt.close()
'''

#Popolartimes_get_method
pop_result = populartimes.get(YOUR_API_KEY, [search_type], (bound_lower_lat, bound_lower_lng), (bound_upper_lat, bound_upper_lng))
#Result = populartimes.get(YOUR_API_KEY, [search_type], (48.132986, 11.566126), (48.142199, 11.580047))

#output part
#output 'populartimes'
pop_file = './popularResult.json'
pro_pop_file = './proPopularResult.json'
tools.json_write(pop_file,pop_result)
tools.json_file_process(pop_file,pro_pop_file)

#output 'textsearch'
text_file = './textResult.json'
tools.json_write(text_file,text_response.text)