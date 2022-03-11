#!/usr/bin/python
# not modify yet
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

        # 此处文件可以做参数
        text_file = open('text_get_result.json','r',encoding= 'utf-8')
        respond = json.loads(text_file.read())
        record_list = respond['results']

        # place_id,name,formatted_address,geometry,price_level,rating,types,user_ratings_total
        # id,name,add,geo,price,rating,type,user_rating_total

        # declare SQL string for records
        table_name = "test.test_more"
        sql_string = 'INSERT INTO {} '.format(table_name)
        sql_string += "(id,name,add,geo,rating,type,user_rating_total)" 
        
        for i in record_list:
            sql = ''
            # head
            sql_value_string = " VALUES ("
            # id
            sql_value_string += "'" + i['place_id'] + "', "
            # name : ' have to be ''
            name = i['name']
            name = name.replace("'", "''")
            sql_value_string += "'" + name + "', "
            # address
            sql_value_string += "'" + i['formatted_address'] + "', "
            # geo : type:point
            geo = i['geometry']
            loc = geo['location']
            lat_lng = "point(" + str(loc['lat'])+ ", " + str(loc['lng']) + ")"
            sql_value_string += lat_lng + ", "

            # price_level
            #sql_value_string += "'" + str(i['price_level']) + "', "

            # rating
            sql_value_string += "'" + str(i['rating']) + "', "
            # types
            types = i['types']
            tp = types[0]
            sql_value_string += "'" + tp + "', "
            # user rating total
            sql_value_string += "'" + str(i['user_ratings_total']) + "'"
            # tail
            sql_value_string += ")"
            
            sql = sql_string + sql_value_string
            cur.execute(sql)

        #cur.execute("DELETE FROM test.test_more")
        cur.execute("SELECT * FROM test.test_more")
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

