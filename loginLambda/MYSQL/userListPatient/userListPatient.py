import pymysql.cursors
import json
import googlemaps
from datetime import datetime
# from operator import itemgetter
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
    userLat = event['userLat']
    userLong = event['userLong']
    
    cursor = connection.cursor()
    
    sql = "SELECT BloodGroup, RHFactor FROM UserDetails WHERE UserName = '" + userName + "'"
    
    cursor.execute(sql)
    result = cursor.fetchall()
    
    print result
    bloodGroup = result[0]['BloodGroup']
    rhFactor = result[0]['RHFactor']
    

    if bloodGroup == "O" and rhFactor == '+':
        whereClause = "(HPR.BloodGroup = 'O' AND HPR.RHFactor = '+') OR (HPR.BloodGroup = 'A' AND HPR.RHFactor = '+')\
                        (HPR.BloodGroup = 'B' AND HPR.RHFactor = '+') OR (HPR.BloodGroup = 'AB' AND HPR.RHFactor = '+')"
    elif bloodGroup == "A" and rhFactor == '+':
        whereClause = "(HPR.BloodGroup = 'A' AND HPR.RHFactor = '+') OR (HPR.BloodGroup = 'AB' AND HPR.RHFactor = '+')"
    elif bloodGroup == "B" and rhFactor == '+':
        whereClause = "(HPR.BloodGroup = 'B' AND HPR.RHFactor = '+') OR (HPR.BloodGroup = 'AB' AND HPR.RHFactor = '+')"
    elif bloodGroup == "AB" and rhFactor == '+':
        whereClause = "(HPR.BloodGroup = 'AB' AND HPR.RHFactor = '+')"
    elif bloodGroup == "O" and rhFactor == '-':
        whereClause = "1=1"
    elif bloodGroup == "A" and rhFactor == '-':
        whereClause = "(HPR.BloodGroup = 'A'  OR HPR.BloodGroup = 'AB' )"
    elif bloodGroup == "B" and rhFactor == '-':
        whereClause = "(HPR.BloodGroup = 'B'  OR HPR.BloodGroup = 'AB' )"
    elif bloodGroup == "AB" and rhFactor == '-':
        whereClause = "(HPR.BloodGroup = 'AB' )"
    
    sql = "SELECT  PatientID, HPR.BloodGroup, HPR.RHFactor, DATE_FORMAT(PostedDate, '%d-%m-%Y') AS PostedDate, \
            FirstName AS HospitalName, UserLat AS HospitalLat, UserLong AS HospitalLong, HPR.UserName AS HospitalUserName\
            FROM HospitalPostingRequest AS HPR INNER JOIN UserDetails AS UD\
            ON HPR.UserName = UD.UserName \
            WHERE " + whereClause + "AND IsRequired = 1"
    print sql
    
    result = 'success'
    
    cursor.execute(sql)
    result = cursor.fetchall()
    
    origins = list()
    origins.append((userLat, userLong))
    
    destinations = list()
    # print type(result)
    for i in result:
        lat= i['HospitalLat']
        long= i['HospitalLong']
        destinations.append((lat,long))
    
    matrix = gmaps.distance_matrix(origins, destinations)
    
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
            if 'distance' not in rows:
                print 'here1'
                distance =  100000
                result[i]['proximity'] = distance
            else:
                distance =  rows['distance']['value']
                result[i]['proximity'] = distance
                i=i+1
                print result
    # for rows in result:
    newlist = sorted(result, key=lambda row: row['proximity'])
        
    # newlist = sorted(result, key=itemgetter('proximity')) 
    
    a = {}
    a['results'] = newlist
    
    try:
        return a
    except Exception as e: 
        print e
        return str(e)
    else:
        return a