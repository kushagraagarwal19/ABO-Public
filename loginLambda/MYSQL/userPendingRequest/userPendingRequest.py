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
    # Collect the arguments sent by Get Request
    userName = event['userName']
    
    cursor = connection.cursor()
    sql = "SELECT FirstName, LastName, PatientID, DATE_FORMAT(RequestedDate, '%d %m %Y') AS RequestedDate\
           FROM HospitalUserRequest AS HUR \
           INNER JOIN UserDetails AS UD ON HUR.HospitalUserName = UD.UserName \
           WHERE HUR.UserUserName = '" + userName + "' AND HUR.IsActive = 1 \
           AND HUR.IsAcceptedByUser = 0 ORDER BY HUR.RequestedDate DESC"
    print sql
    
    cursor.execute(sql)
    result = cursor.fetchall()
        
    # print type(result)
    # print result[0]
    # result = json.dumps(result)
    # print(result)
    
    # result = json.loads(result)
    # print result
    
    # print type(result)
    if len(result) == 0:
        return "No pending requests"
    # return str(result)
    print type(result)
    print 'hello'
    return result