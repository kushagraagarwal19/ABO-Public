import pymysql.cursors
import hashlib
import json
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
    userPassword = event['userPassword']
    
    # print("username from front is "+ userName)
    # print("pass from front is "+ userPassword)
    # print("type from front is "+ userType)
    
    
    h = hashlib.new('md5')
    h.update(userPassword)
    userPassworHash = str(h.hexdigest())
    
    # print type(userPassworHash)
    # print type(h.digest())
    # print("userpasshash is " + userPassworHash)
    
    cursor = connection.cursor()
    with connection.cursor() as cursor:
        sql = "SELECT UserPassword, UserType FROM UserLoginDetails WHERE UserName = '" + userName + "'"
        print sql
        cursor.execute(sql)
        result = cursor.fetchone()
        
        # Check whether useranme exists or not!
        if result is None:
            return "UserName doesn't exist"
        
        passwordHash = result['UserPassword']
        userType = result['UserType']
        print passwordHash
        
        error = {"message" : "password is wrong"}
        response = {"usertype" : userType}
        
        if userPassworHash != passwordHash:
            # return json.dumps("UserPassword is wrong")
            return error
        else:
            return response