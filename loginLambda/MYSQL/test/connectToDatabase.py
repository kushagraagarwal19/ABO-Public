import pymysql.cursors

def lambda_handler(event, context):
    connection = pymysql.connect(host='dbinstance.ct0jj0n9ijm8.us-east-1.rds.amazonaws.com',
                                user='masterusername',
                                password='masterpassword',
                                db='BloodBank',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()

    with connection.cursor() as cursor:
        sql = "select * from UserLoginDetails"
        cursor.execute(sql)
        rows = cursor.fetchall()

        # print rows
        for row in rows:
            print(row['UserName'], row['UserPassword'], row['UserType'])

# Insert into dbo.logindetails values ('user1', 'userpass1', 'hospital'), ('user2', 'userpass2', 'individual')
    return 'Hello from Lambda'