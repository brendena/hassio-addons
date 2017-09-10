from googleSheetUpload import GoogleSheetUpload
import sys
import json
from datetime import date, timedelta, datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

# the apscheduler need the logger
# to be configured
# https://stackoverflow.com/questions/17528363/no-handlers-could-be-found-for-logger-apscheduler-scheduler
logging.basicConfig()
scheduler = BlockingScheduler()


#if any agruments
if len(sys.argv) != 1:
	print("number of arguements " + str(len(sys.argv)))
	print("proper amount of arguments 1")
	sys.exit(0)

	
	

with open("/data/options.json") as configFile:
	configData = json.load(configFile)


loopTimeAmount = configData["time"] #time in hours
uploadJson = configData["upload"] #json string


'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/
/		The conversion uploadJson to googleSheets

/
/	Below code convert it from the config style
/	to a dict of sheetName with values of entityList
/	"upload":[
/			{"sheetName": "testName",
/			  "entityList":"media_player.roku"
/			},
/			{"sheetName": "testName",
/			  "entityList":"sun.sun"
/			}
/		]
/		
/		to
/	upload = {
/		sheetName: ["media_player.roku", "sun.sun"]
/     }
/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
#global values
googleSheets = {} 
for option in uploadJson:
	if(option["sheetName"] in googleSheets):
		googleSheets[option["sheetName"]].append(option["entity"])
	else:
		googleSheets[option["sheetName"]] = [option["entity"]]


googleSheetUploader = GoogleSheetUpload()
start = datetime.now()
end = datetime.now()

print("started program at " + str(start.strftime("%Y-%m-%d %H:%M:%S")))

@scheduler.scheduled_job('interval', hours=loopTimeAmount)
def entireLoop():
	'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	/		Way the timer works
	/	start = > end
	/			  start = > end
	/						start = > end
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
	global start
	global end
	global googleSheets
	global googleSheetUploader
	start = end
	end = datetime.now()
	
	
	print("loopinging through")	

	for googleSheetName in googleSheets:
		print(googleSheetName)
		googleSheetUploader.changeSheetAndEntities(googleSheetName, googleSheets[googleSheetName])
		googleSheetUploader.updateGoogleSheet(start,end)
	print("start")
	print(start.strftime("%Y-%m-%d %H:%M:%S"))
	print("end")
	print(end.strftime("%Y-%m-%d %H:%M:%S"))
	print("done")
		
		


scheduler.start()

	



#python index.py 10 '{"time":1,"upload":[{"sheetName":"TestBed", "entity": "media_player.kitchen_home"},{"sheetName":"TestBed", "entity": "media_player.roku_1gu4a2104295"}]}'
