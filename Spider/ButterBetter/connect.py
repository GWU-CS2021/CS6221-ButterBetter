import searchPopularity as sp
import searchText as st
import tools
import json
import connect

# Google API KEY
API_KEY = 'xx'
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
input_text_2 = 'restaurants nearby Georgetown'
# Text search file
text_file_path = './text_result/'
text_file_1 = '1.json' 
text_file_2 = '2.json'
text_file_3 = '3.json' 
text_file_4 = '4.json'
text_file_5 = '5.json' 
text_file_6 = '6.json' 

def get_token(file_name):
    f = open(text_file_path + file_name, 'r', encoding= 'utf-8')
    respond = json.loads(f.read())
    if 'next_page_token' in respond.keys():
        token = respond['next_page_token']
    else:
        token = None
        print(file_name + ' has no next page token')
    f.close()
    return token

'''
# Searching for 1ed page
result = st.search_by_text_to_json(API_KEY, input_text, text_file_path + text_file_1, radius)

# Searching for 2ed page
token = get_token(text_file_1)
result = st.search_by_token_to_json(API_KEY, token, text_file_path + text_file_2)

# Searching for 3rd page
token = get_token(text_file_2)
result = st.search_by_token_to_json(API_KEY, token, text_file_path + text_file_3)

# Searching for 4ed page
#result = st.search_by_text_to_json(API_KEY, input_text_2, text_file_path + text_file_4, radius)

# Searching for 5ed page
token = get_token(text_file_4)
result = st.search_by_token_to_json(API_KEY, token, text_file_path + text_file_5)
'''

# Text_search -> id -> popularity_search
# The final search result is in ./pop_result/
# Popularity search file
def get_pop_results(text_file_name,page):
    f = open(text_file_path + text_file_name, 'r', encoding= 'utf-8')
    respond = json.loads(f.read())
    f.close()
    results = respond['results']
    pop_file_path = './pop_result/'
    index = (page - 1) * 20 + 1
    for i in results:
        file_name = str(index) + '.json'
        pop_file = pop_file_path + file_name
        result = sp.get_id_to_json(API_KEY,i['place_id'],pop_file)
        index += 1

#get_pop_results(text_file_1,1)
#get_pop_results(text_file_2,2)
#get_pop_results(text_file_3,3)
#get_pop_results(text_file_4,4)
#get_pop_results(text_file_5,5)

# pop results checking
'''
for i in range(1,101):
    pop_file_path = './pop_result/'
    file_name = str(i) + '.json'
    f = open(pop_file_path + file_name, 'r', encoding = 'utf-8')
    respond = json.loads(f.read())
    f.close()
    id = respond['id']
    name = respond['name']
    print(str(i) + '   ' + id + '   ' + name)
'''

connect.connect()







