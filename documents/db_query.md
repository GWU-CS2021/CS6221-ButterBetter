## Get User

```sql
select user_name,user_location_point,user_location_full from public.user where user_id = %s"
```

`s1 = (get_md5(user_id))`

- return
  - user_name
    - MD5 value of alexa device id
  - user_location_point
    - Geo coordinates of user location
  - user_location_full
    - User location in readable text

## Add User

```sql
insert into public.user (user_id,user_name,user_location_point,user_location_full) values (%s,%s,point(%s, %s),%s ) on CONFLICT(user_id) DO Update set user_name = excluded.user_name,user_location_point=excluded.user_location_point,user_location_full=excluded.user_location_full
```

`s1 = (get_md5(user_id))`

`s2= name_from_voice`

`s3 = geo_coord["lat"]`

`s4 = geo_coord["lng"]`

`s5 = address formatted`

## Get Restaurant

```sql
select id,name,address_geo,address,close_hour,tel from public.restaurant where {filter1} order by {filter2} limit 10
```

- filter1

- ```sql
  open_hour < HOUR(current_timestamp) and HOUR(current_timestamp)< HOUR(current_timestamp-3600) |
  type = {selected type}
  ```

  

- filter2

- ```sql
  score = 
  {pricing:price_level*1000}+
  {distance:ST.distance(address_geo,user.user_location_point)*5}+
  {wait_time:popular_hour(timestamp.now)*10}+
  {rating:user_rating*1000}
  order by score asc
  ```

  

- return
  - id
    - restaurant unique id
  - name
    - restaurant name formatted
  - address_geo
    - restaurant geo coordinates
  - address
    - restaurnat address readable
  - close_hour
    - restaurant expected close hour
  - tel
    - restaurant telephone

## Get Review

```sql
select user_name,rating,review from public.reviews
```

- return
  - user_name
    - user who submitted this review
  - rating
    - rating point out of 5
  - review
    - review in text

