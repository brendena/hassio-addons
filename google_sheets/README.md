# Results
![alt text](./SpreadSheetOutputExample.png)

This is a Hass.io add-on to upload the state of a entity given a set interval of time to upload.  You can have multiple entities and upload to multiple different spreadsheets.  For Each entity it will create a separate sheet to avoid having timing conflicts.

# Geating started


## 1 Get google drive Credentials
Follow the first parts of this [tutorial](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)

It will show you how to go to google API Console and create a google service.  At the end you will get a client_secret.json file.

You want to put that file inside your

/share - directory inside of HASS.io

then rename the file to googleDriveCredentials.json


## 2 Share the spreed sheet with your service

First you have to create a spread sheet that you want your information to be added to and then share it with the service you just created.

Inside of your googleDriveCredentials.json there should a email.  It is this email that you want to share your spreadsheet with.

## 3 You want to go the hass.io and configer app
![alt text](./ConfigExample.png)

Example of my Set up

time - Is the Amount of time before its going to refresh google spreesheets

Example 0.5 = 30 minites

upload - is a array entitys that you want to uplaod and what spreadsheet you want to upload them to 

sheetName - is the name of your shared spreesheet

entity - is the entity title of you item.


