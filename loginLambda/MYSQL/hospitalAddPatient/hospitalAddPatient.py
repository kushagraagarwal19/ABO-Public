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
    patientName = event['patientName']
    bloodGroup = event['bloodGroup']
    rhFactor = event['rhFactor']
    
    cursor = connection.cursor()
    sql = "INSERT INTO HospitalPostingRequest (Username, PatientName, BloodGroup, RHFactor, IsRequired, PostedDate)\
            VALUES ('" + userName + "' , '" + patientName + "' , '" + bloodGroup + "' , '" + rhFactor + "' , 1, NOW())"
    print sql
    
    try:
        cursor.execute(sql)
    except Exception as e: 
        return str(e)
    else:
        return 'Success'