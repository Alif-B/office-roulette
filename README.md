# Office Roulette

A roulette betting table for the people in my office. Coworkers can bet on The Wheel of Blame
It is only designed for the people at my office so only they can play the game at http://wheelofblame.click/


## Infrastructure
Policies have been set according to the needs of service actions.
* AWS Route53 hosted zone routes the traffic to S3 -->
* Web application (frontend) deployed on `AWS S3 Static Hosting` -->
* Which then sends requests to an `AWS API Gateway` -->
* API Gateway forwars it to an `AWS Lambda funtions` -->
* Lambda gets the password stored in `AWS Secrets Manager` <--
* Lambda then compares the password stored in secrests manager to the entered one ...
* If passwords match then Lambda CRUDs data in `AWS DynamoDB` <-->


## Reminder

Virutal Environmnets have been gitignored. So I need to install the dependencies when running this on a new environment.  
SSL Certificate not applied cause I don't want to pay `AWS Certificates Manager`
