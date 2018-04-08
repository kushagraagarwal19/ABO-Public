import pymysql.cursors
import hashlib

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
    firstName = event['firstName']
    lastName = event['lastName']
    userPassword = event['userPassword']
    userType = event['userType']
    userLat = event['userLat']
    userLong = event['userLong']
    
    h = hashlib.new('md5')
    h.update(userPassword)
    userPassworHash = str(h.hexdigest())
    
    cursor = connection.cursor()
    sql = "SELECT UserName FROM UserLoginDetails WHERE UserName = '" + userName + "'"
    # print sql
    cursor.execute(sql)
    result = cursor.fetchone()
    
    # Check whether useranme exists or not!
    if result is not None:
        return "This UserName already exists"
    
    sql = "INSERT INTO UserLoginDetails VALUES ('" + userName + "' , '" + userPassworHash + "' , '" + userType + "')"
    # print sql
    cursor.execute(sql)
    
    sql = "INSERT INTO UserDetails VALUES ('" + userName + "' , '" + firstName + "' , '" + lastName + "' , " + str(userLat) + " , " + str(userLong) + ")"
    # print sql
    cursor.execute(sql)
    
    return "Success"