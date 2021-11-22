import populartimes
import json

#function PreJson
def PreJson(filename):
    f = open(filename, 'r')
    content = eval(f.read())
    f.close()
    p_content = json.dumps(content,sort_keys = False, indent = 2)
    f = open('Pre'+filename, 'w')
    f.write(p_content)
    f.close()

#Google API KEY
YOUR_API_KEY = 'AIzaSyC4DMtNlVt4fQrDry1SJU4AtwE6750x61c'
#Type of searching ([str] example: [restaurant])
SearchType = "restaurant"
#Test current location as GWU in Google Map (38.899793, -77.048584)
CurrentLat = 38.899793
CurrentLng = -77.048584
#Set param for bound
BoundLowerLat = CurrentLat-0.005
BoundLowerLng = CurrentLng-0.02
BoundUpperLat = CurrentLat+0.005
BoundUpperLng = CurrentLng+0.02
#Set radius
Radius = 50000

'''
Result = populartimes.get_id(YOUR_API_KEY, "ChIJSYuuSx9awokRyrrOFTGg0GY")

ResultTxt = open('resultGetid.json', 'w')

ResultJS = json.dumps(Result)
ResultTxt.write(ResultJS)

ResultTxt.close()
'''

#Popolartimes_get_method
Result = populartimes.get(YOUR_API_KEY, [SearchType], (BoundLowerLat, BoundLowerLng), (BoundUpperLat, BoundUpperLng))
#Result = populartimes.get(YOUR_API_KEY, [SearchType], (48.132986, 11.566126), (48.142199, 11.580047))
ResultTxt = open('resultGet.json', 'w')

ResultJS = json.dumps(Result)
ResultTxt.write(ResultJS)

ResultTxt.close()

PreJson('resultGet.json')
