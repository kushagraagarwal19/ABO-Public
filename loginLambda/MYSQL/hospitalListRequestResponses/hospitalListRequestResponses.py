import pymysql.cursors
import json
import googlemaps
from datetime import datetime

# import hashlib

gmaps = googlemaps.Client(key='AIzaSyDZhjxJiq0hcDiB1MDGBAO12RBB7tBIB5k')

connection = pymysql.connect(host='dbinstance.ct0jj0n9ijm8.us-east-1.rds.amazonaws.com',
                            user='masterusername',
                            password='masterpassword',
                            db='BloodBank2',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
                            
def lambda_handler(event, context):
    # Collect the arguments sent by Post Request
    userName = event['userName'] 
    
    cursor = connection.cursor()
    
    sql = "Select PatientName AS pName, HUR.PatientID AS pId, CONCAT(FirstName, ' ', LastName) AS userName, \
            UserUserName AS userId, RequestID AS rId, UserLat AS lat, UserLong AS lon FROM\
            HospitalUserRequest AS HUR INNER JOIN UserDetails AS UD \
            ON UD.UserName = HUR.UserUserName\
            INNER JOIN HospitalPostingRequest AS HPR\
            ON HPR.PatientID = HUR.PatientID\
            WHERE HospitalUserName = '" + userName + "' AND IsActive = 1\
            AND IsAcceptedByHospital = 0 AND IsRejectedByHospital = 0"
    print sql
    
    cursor.execute(sql)
    result = cursor.fetchall()
    
    destinations = list()
    print type(result)
    for i in result:
        lat= i['lat']
        long= i['lon']
        destinations.append((lat,long))
    print destinations
    
    if len(result) == 0:
        return "fail"
    
    sql = "SELECT UserLat, UserLong FROM UserDetails WHERE UserName = '" + userName + "'"
    cursor.execute(sql)
    originresult = cursor.fetchall()
    
    initLat = originresult[0]['UserLat']
    initLong = originresult[0]['UserLong']
    
    origins = list()
    origins.append((initLat, initLong))
    
    print origins
    if origins is None or destinations is None:
        return "fail"
    matrix = gmaps.distance_matrix(origins, destinations)
    
    print json.dumps(matrix)
    
    
    if 'distance' not in matrix['rows'][0]['elements'][0]:
        print "LOL"
        print matrix
    else:
        i = 0
        print matrix
        print json.dumps(matrix)
        for rows in matrix['rows'][0]['elements']:
            print 'HI'
            print rows
            distance =  rows['distance']['value']
            result[i]['proximity'] = distance
            i=i+1
            print result
    
    newlist = sorted(result, key=lambda k: k['proximity'])
    
    a = {}
    a['results'] = newlist
    
    try:
        cursor.execute(sql)
    except Exception as e: 
        print e
        return str(e)
    else:
        return a