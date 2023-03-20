# AWS to Qualtrics Data Connection Script Overview
The AWS to Qualtrics data connection is a python script that was developed to provide a secure, seamless 
process for transferring Village of Widsom's Culturally Affirming Climate Survey (CACS) data over to Discriminology’s AWS database.
We accomplish this by using the Qualtrics API, a python script, and an AWS S3 bucket.

Definitions
- Qualtrics API: the Qualtrics API (application programming interface) provides a way for the Qualtrics platform to communicate with other platforms (e.g. AWS)
- Python Script: a list of computer code telling the computer what to do
- AWS S3 Bucket: a digital container for safely storing, protecting, and retrieving data with Amazon Web Services (AWS)

Using a python script, we connect to the Qualtrics API to access Village of Wisdom’s Qualtrics account and data. 
Once the connection is made, we retrieve data from Village of Wisdom’s Qualtrics account. Using the same python script, we 
connect to Disciminology’s AWS S3 bucket and store the retrieved data.
