import searchPopularity as sp
import searchText as st
import tools
import json

# Google API KEY
API_KEY = 'AIzaSyC4DMtNlVt4fQrDry1SJU4AtwE6750x61c'
# Type of searching ([str] example: [restaurant])
search_type = "restaurant"
# Test current location as GWU in Google Map (38.899793, -77.048584)
current_lat = 38.899793
current_lng = -77.048584
# Set param for bound
bound_lower_lat = current_lat - 0.00025
bound_lower_lng = current_lng - 0.001
bound_upper_lat = current_lat + 0.00025
bound_upper_lng = current_lng + 0.001
# set radius
radius = 5000
# Text search input text
input_text = 'restaurants nearby GWU'
# Text search file
text_file  = './text_search_result.json' 
# Popularity search file
pop_file = './popularity_result.json'


#result = st.search_by_text(API_KEY, input_text, text_file, radius)
f = open(text_file,'r', encoding= 'utf-8')
respond = json.loads(f.read())

# Searching for 2ed page
#token = respond['next_page_token']
#result = st.search_by_token_to_json(API_KEY, token, './page2.json')


results = respond['results']

# Example of searching data
'''
for i in results:
    print('Address' + i['formatted_address'])
    print('Name'+ i['name'])
    print('ID'+ i['place_id'])
'''

# Search id by resturant name
def search_id_by_name(name):
    for i in results:
        if i['name'] == name:
            return i['place_id']
        else:
            return None

id = search_id_by_name('North Italia')

# Text_search -> id -> popularity_search
if(id != None):
    result = sp.get_id_to_json(API_KEY,id,pop_file)
    print(result)






