import pymysql.cursors
import json
# import hashlib

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
    
    sql = "SELECT PatientName, BloodGroup, RHFactor, DATE_FORMAT(PostedDate, '%d-%m-%Y') AS PostedDate\
            FROM HospitalPostingRequest\
            WHERE IsRequired = 1 AND UserName = '" + userName + "'" 
    print sql
    
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e: 
        print e
        return str(e)
    else:
        return result