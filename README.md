# ABO-Public
This is the public repository of the ABO (Blood Bank project) done in the Cloud Computing class.

## What is it?:
The idea of this project is to provide a platform to the users (who wants to donate blood) so that they can donate it more conveniently. It connects users to the hospitals. Hospitals post the request and user respond to the requests posted by the hospitals.

## Technologies:
This was built as an iOS app using various AWS services - [SES](https://aws.amazon.com/ses/), [Lambda](https://aws.amazon.com/lambda/), [RDS](https://aws.amazon.com/rds/), [API Gateway](https://aws.amazon.com/api-gateway/), and [CloudWatch](https://aws.amazon.com/cloudwatch/). [Google Distane Matrix](https://developers.google.com/maps/documentation/distance-matrix/intro) in [Python](https://github.com/googlemaps/google-maps-services-python) was used to calculate distance between the user and the hospital.

## My Contribution:
I designed the backend architecture and wrote Lambda functions in oder to access the database tables. Also designed the API Gateway (methods and resources) and linked them with the Lambda Functions

Don't forget to check the [demo video](https://www.youtube.com/watch?v=oCwN1TXu8Rc) as well!
