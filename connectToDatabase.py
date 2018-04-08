import pymysql.cursors
import json

connection = pymysql.connect(host='dbinstance.ct0jj0n9ijm8.us-east-1.rds.amazonaws.com',
                             user='masterusername',
                             password='masterpassword',
                             db='BloodBank2',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

# sql = "INSERT INTO BloodBank2.UserLoginDetails VALUES ('username45', '819b0643d6b89dc9b579fdfc9094f28e', 'Hospital')"
# cursor.execute(sql)
# # row = cursor.fetchone()
# connection.commit()

# sql = "INSERT INTO UserDetails VALUES ('" + userName + "' , '" + firstName + "' , '" + lastName + "' + "' , '" + '" str(userLat) + " , " + str(userLong) + ")"

# print row
print "inseryuetv"

sql = "SELECT UserName, FirstName FROM UserDetails"
cursor.execute(sql)
result = cursor.fetchone()

# result = json.loads(result)

print type(result)
print result['UserName']

    # row = cursor.fetchone()

    # print row
    # rows = cursor.fetchone()
    # if rows is None:
    #     print 'pappu'
    # print len(rows)

    # print type(rows)
    # print rows
    # print(rows['UserName'])
        