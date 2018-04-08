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
    patientID = event['patientID']
    
    cursor = connection.cursor()
    
    sql = "UPDATE HospitalPostingRequest SET IsRequired = 0 WHERE PatientID = " + str(patientID)
    print sql
    
    result = 'success'
    
    try:
        cursor.execute(sql)
    except Exception as e: 
        print e
        return str(e)
    else:
        return result