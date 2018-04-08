import pymysql.cursors
import json
import boto3
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
    hospitalUserName = event['hospitalUserName']
    userName = event['userName']
    patientID = event['patientID']
    
    cursor = connection.cursor()
    
    sql = "SELECT BloodGroup, RHFactor FROM UserDetails WHERE UserName = '" + userName + "'"
    
    cursor.execute(sql)
    result = cursor.fetchall()
    
    print result
    bloodGroup = result[0]['BloodGroup']
    rhFactor = result[0]['RHFactor']
    
    sql = "SET SQL_SAFE_UPDATES = 0;\
            INSERT INTO HospitalUserRequest (HospitalUserName, UserUserName, PatientID, \
            BloodGroup, RHFactor, IsActive, IsAcceptedByHospital, RequestedDate, IsRejectedByHospital)\
            VALUES ('" + hospitalUserName + "' , '" + userName + "' , " + str(patientID) + " , '" + bloodGroup + "' , \
            '" + rhFactor + "' , 1, 0, NOW(), 0);"
    print sql
    
    cursor.execute(sql)
    
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "ka1745@nyu.edu"
    
    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = "success@simulator.amazonses.com"
    
    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    CONFIGURATION_SET = "ConfigSet"
    
    # The subject line for the email.
    SUBJECT = "Hi, Someone Responed to your request
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Hi,\r\n"
                 "Someone responed to your request")
                
    
    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses')
    
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['ResponseMetadata']['RequestId'])
    
    try:
        return "success"
    except Exception as e: 
        print e
        return str(e)
    else:
        return "success"