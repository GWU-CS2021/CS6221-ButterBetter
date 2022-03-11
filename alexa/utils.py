import datetime
import logging
import os
import boto3
import requests
import json
import psycopg2
import hashlib
from botocore.exceptions import ClientError

key = 'xx'
chat_id = -1001275440586


class RestInfo:
    def __init__(self, title, addr, tel, lat, lon, open_time, close, pop, price, rating, rest_id, types, dist):
        self.title = title
        self.addr = addr
        self.tel = tel
        self.lat = lat
        self.lon = lon
        self.open_time = open_time
        self.close = close
        self.pop = pop
        self.price = price
        self.rating = rating
        self.rest_id = rest_id
        self.type = types
        self.dist = dist


def get_time_str(hour_int):
    if hour_int < 13:
        close_time_str = str(hour_int)
    else:
        close_time_str = str(hour_int - 12)
    if hour_int >= 12:
        close_time_str = close_time_str + " p.m. "
    else:
        close_time_str = close_time_str + " a.m. "
    return close_time_str

def send_to_phone(user, rest_info):
    url = "https://api.telegram.org/bot2142892818:xx/sendMessage"
    price_icon = "$"
    for i in range(0,rest_info["price"]-1):
        price_icon = price_icon+"$"
    textes = "<b>User %s request</b>\n" \
             "<b>%s</b>\n" \
             "<b>Type</b>: %s, %s\n" \
             "<b>Tel</b>: %s\n" \
             "<b>Time</b>: %02d:00-%02d:00\n" \
             "<b>Address</b>: %s" % (user,rest_info["title"], rest_info["type"], price_icon, rest_info["tel"].replace(" ", "-"), rest_info["open_time"], rest_info["close"], rest_info["addr"])
    params = {"chat_id":chat_id,
              "parse_mode":"html",
              "text":textes}

    response = requests.request("GET", url, params=params)
    print(response.text)
    location_url = "https://api.telegram.org/bot2142892818:xx/sendVenue"
    params = {"chat_id":chat_id,
              "latitude":rest_info["lat"],
              "longitude":rest_info["lon"],
              "title":rest_info["title"],
              "address":rest_info["addr"],
              "google_place_id":rest_info["rest_id"]}
    response = requests.request("GET", location_url, params=params)
    print(response.text)


#send_to_phone("roger", RestInfo("Chef Geoff's West End", "2201 M St NW, Washington, DC 20037, United States", "+1 202-524-7815",
                                #38.9053839, -77.0491591, 9, 23, 10, 4, 4.5,"ChIJtzxgmCa3t4kRosPkvNfA0XE","American"))
def create_presigned_url(object_name):
    """Generate a presigned URL to share an S3 object with a capped expiration of 60 seconds

    :param object_name: string
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = boto3.client('s3',
                             region_name=os.environ.get('S3_PERSISTENCE_REGION'),
                             config=boto3.session.Config(signature_version='s3v4',s3={'addressing_style': 'path'}))
    try:
        bucket_name = os.environ.get('S3_PERSISTENCE_BUCKET')
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=60*1)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def get_pgconn():
    return psycopg2.connect("host=xx dbname=postgres user=postgres password=xx")


def get_md5(custom_string):
    uid_md5 = hashlib.md5(custom_string.encode())
    return uid_md5.hexdigest()


def get_geo_with_address(address_string):
    """get geo coordinates with google map"""
    url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {'address': address_string, 'key': key , 'location': '38.900,-77.039'}

    response = requests.request("GET", url, params=params)
    if response.status_code >= 400:
        print("error "+response.text)
        return False, "", ""
    resp = json.loads(response.text)
    if len(resp["results"]) != 0:
        return True, resp["results"][0]["geometry"]["location"], resp["results"][0]["formatted_address"]
    return False, "", ""


def add_user_record(user_id, name, address_string):
    valid, geo_coord, addr = get_geo_with_address(address_string)
    if not valid:
        return False
    conn = get_pgconn()
    cur = conn.cursor()
    try:
        cur.execute("insert into public.user (user_id,user_name,user_location_point,user_location_full) values "
                    "(%s,%s,point(%s, %s),%s ) on CONFLICT(user_id) DO Update set user_name = excluded.user_name,"
                    "user_location_point=excluded.user_location_point,user_location_full=excluded.user_location_full"
                    , (get_md5(user_id), name, geo_coord["lat"], geo_coord["lng"], addr))
    except Exception as e:
        print(e)
        return False
    conn.commit()
    cur.close()
    conn.close()
    return True


# user_id -> exist,name,point(lat,lng),addr
def check_user_exist(user_id):
    conn = get_pgconn()
    cur = conn.cursor()
    cur.execute("select user_name,user_location_point,user_location_full from public.user where user_id = %s",
                (get_md5(user_id),))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if not result:
        return False, "", "", ""
    return True, result[0], result[1], result[2]


def get_review(restaurant_id):
    conn = get_pgconn()
    cur = conn.cursor()
    sql = "select name,review_text,review_user,review_rating from test.review where review_rating != 0 and place_id = '%s'"%restaurant_id
    cur.execute(sql)
    result = cur.fetchall()
    if len(result) == 0:
        return False,"","","",""
    cur.close()
    conn.close()
    return True,result[0][0],result[0][1],result[0][2],result[0][3]


def get_restaurant(user_id, pref_1, pref_2, types):
    conn = get_pgconn()
    cur = conn.cursor()
    price_modifier = 1000
    busy_modifier = 100
    rating_modifier = 1000
    distance_modifier = 2000
    if pref_1 == 'busy' or pref_2 == 'busy':
        busy_modifier *= 5
    if pref_1 == 'cheap' or pref_2 == 'cheap':
        price_modifier *= 5
    if pref_1 == 'best' or pref_2 == 'best':
        rating_modifier *= 5
    if pref_1 == 'near' or pref_2 == 'near':
        distance_modifier *= 5
    order_string = "price_level*%d+rest.busy*%d+rest.user_rating*%d+miles*%d" %\
                   (price_modifier,busy_modifier,rating_modifier,distance_modifier)
    sql = '''select rest.place_id,rest.place_name,rest.add,rest.open_hour,rest.close_hour,rest.tel,geo[0],geo[1],price_level,user_rating,miles,busy from (
select rest.*,u.user_location_point,SQRT(POW(69.1 * (user_location_point[0]::float -  geo[0]::float), 2) +
    POW(69.1 * (geo[1]::float - user_location_point[1]::float) * COS(user_location_point[0]::float / 57.3), 2)) as miles from
(select place_id,place_name,add,open_hour,close_hour,tel,geo,busy_'''+"%02d"%(datetime.datetime.now().hour)+''' as busy,price_level,user_rating from test.final
where date_part('hour',current_timestamp-interval '5 hour')>= open_hour and date_part('hour',current_timestamp-interval '5 hour')< close_hour
and types like '%'''+types+'''%') rest join (select user_location_point from public.user where user_id = '''+"'"+user_id+"'" +''') u on 1=1
)rest order by '''+order_string
    print(sql)
    cur.execute(sql)
    result_arr = []
    for result in cur.fetchall():
        #result_arr.append(RestInfo(result[1],result[2],result[5],result[6],result[7],result[3],result[4],0,result[8],result[9],result[0],types,result[10]))
        result_arr.append(
            {"title":result[1],
             "addr":result[2],
             "tel":result[5],
             "lat":result[6],
             "lon":result[7],
             "open_time":result[3],
             "close":result[4],
             "pop":result[11],
             "price":result[8],
             "rating":result[9],
             "rest_id":result[0],
             "type":types,
             "dist":result[10]})
        print(result)

    #send_to_phone("roger",result_arr[0])
    cur.close()
    conn.close()
    return result_arr

# print(check_user_exist("aabbccd"))
#add_user_record("aabbccd","roger","1900 half st sw")
# get_geo_with_address("1900 half st sw")
#get_restaurant('e233d84bf19d72952aec3da4c009724c','cheap','near','american')


#print(get_review("ChIJpQ0Bnkm2t4kRd-wm0hZLeCc"))

#send_to_phone("roger",
#              {'title': 'Dish + Drinks', 'addr': '924 25th St NW, Washington, DC 20037, United States', 'tel': '+1 202-338-8708', 'lat': 38.9014311, 'lon': -77.05370909999999, 'open_time': 0, 'close': 22, 'pop': 0, 'price': 2, 'rating': '4.4', 'rest_id': 'ChIJeys3p7O3t4kRYgii7tUyv1c', 'type': 'american', 'dist': 0.11345419343746714}
#)
