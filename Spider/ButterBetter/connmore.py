#!/usr/bin/python
import json, sys
import psycopg2
from config import config

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        sql_string = ""
        sql_value_string = ""
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)		
        # create first cursor
        cur = conn.cursor()
        
	    # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # get text_file
        file_name = 'get_result.json'
        text_file = open(file_name,'r',encoding= 'utf-8')
        respond_list = json.loads(text_file.read())
        #the respond of this .json is a list
        #record_list = respond['results']

        # place_id,name,formatted_address,geometry,price_level,rating,types,user_ratings_total
        # id,name,add,geo,price,rating,type,user_rating_total

        # declare SQL string for records
        table_name = "public.pop_restaurants"
        sql_string = 'INSERT INTO {} '.format(table_name)
        '''
        sql_string += "(id,name,short,address,types,address_geo,user_rating,user_rating_total,price_level,image_url," 
        sql_string += "refresh_url,tel,tags,open_hour,close_hour)"
        '''
        sql_string += "(id,name,address,types,address_geo,user_rating,user_rating_count,open_hours,close_hours)"
        #sql_string += "tel)"
        for i in respond_list:
            sql = ''
            # head
            sql_value_string = " VALUES ("

            # id
            sql_value_string += "'" + i['id'] + "', "

            # name : ' have to be ''
            name = i['name']
            name = name.replace("'", "''")
            sql_value_string += "'" + name + "', "

            '''
            # short
            short = None
            sql_value_string += "'" + short + "', "
            '''

            # address
            sql_value_string += "'" + i['address'] + "', "

            # types
            types = i['types']
            tp = types[0]
            sql_value_string += "'" + tp + "', "

            # address_geo : type:point
            geo = i['coordinates']
            lat_lng = "point(" + str(geo['lat'])+ ", " + str(geo['lng']) + ")"
            sql_value_string += lat_lng + ", "

            # user_rating
            sql_value_string += "'" + str(i['rating']) + "', "
            #sql_value_string += "int(" + str(i['rating']) + "), "

            # user_rating_count
            sql_value_string += "'" + str(i['rating_n']) + "', "

            '''
            #price_level
            p_l = "default"
            sql_value_string += "'" + p_l + "', "

            #image_url
            i_u = "default"
            sql_value_string += "'" + i_u + "', "

            #refresh_url
            r_u = "default"
            sql_value_string += "'" + r_u + "', "
            '''

            #open_hours eg 10
            open_hour = "10"
            sql_value_string += "'" + open_hour + "', "

            #close_hours eg 22
            close_hour = "22"
            sql_value_string += "'" + close_hour + "'"

            '''
            #tel (data loss for one store and cause error when you add this)
            if ('international_phone_number' in i):
                sql_value_string += "'" + i['international_phone_number'] + "'"
            else:
                sql_value_string += "'" + "None" + "'"
            '''

            # tail
            sql_value_string += ")"
            
            sql = sql_string + sql_value_string
            #print(sql)
            cur.execute(sql)

        #cur.execute("DELETE FROM test.test_more")
        cur.execute("SELECT * FROM "+table_name)
        exe_result = cur.fetchone()
        conn.commit()
        print(exe_result)
        

	    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    connect()

