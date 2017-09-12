#spreadSheets - is the spreadSheet Document
#Sheets and WorkSheets - are the subparts of a spreadSheet Document
import sqlite3
import gspread
import math
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetUpload:
	def __init__(self):
		self.spreadSheetTitle = None
		self.entities = None
		self.__gc = None
		self.__spreadSheet = None
		self.__currentWorkSheet = None
		self.__conn = None
		self.__selectAttributes = ['created', 'state']
		
		
	def changeSheetAndEntities(self,spreadSheetTitle, entities):
		self.spreadSheetTitle = spreadSheetTitle
		self.entities = entities
		
	def updateGoogleSheet(self,startTime,endTime):
		self.__connectGoogle()
		self.__connectToDataBase()
		self.__spreadSheet = self.__gc.open(self.spreadSheetTitle)
		cursor = self.__conn.cursor()
		workingSheetCreated = False
		currentPosition = 0
		'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		/loop through all the entities and
		/append or create to there own
		/Personal sheet
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
		for entity in self.entities:
			#create sheet if there is none
			if(self.__checkSheetsCreated(entity) == False):
				self.__currentWorkSheet = self.__spreadSheet.add_worksheet(title=entity, rows="100", cols="10")
				workingSheetCreated = True
			else:
				self.__currentWorkSheet = self.__spreadSheet.worksheet(entity)
				workingSheetCreated = False
			#get data
			listRowsData = list(cursor.execute(self.__createSQLStatement(entity,startTime,endTime)))
			print("lenght data")
			print(len(listRowsData))
			
			#check to see if the received data's empty
			if(len(listRowsData) != 0):
					
				
				currentPosition = 0
				if(workingSheetCreated == False):
					#get last position
					currentPosition = self.__getPositionLastActiveRow()
				#if google sheet is defined but there no information
				# current position will be -1 and will need to be created
				if(workingSheetCreated == True or currentPosition == -1):
					self.__uploadHeader()
					currentPosition = 2
				
				self._addExtraRows(currentPosition,len(listRowsData))
				
				#Update cell in batch form
				cell_list = self.__currentWorkSheet.range('A'+str(currentPosition) + ':B'+str(currentPosition + len(listRowsData)))
				for rowNumber,rowData in enumerate(listRowsData):
					indexCell_list = rowNumber * 2
					for i, attribute in enumerate(self.__selectAttributes):
						cell_list[indexCell_list + i].value =  rowData[i]
				self.__currentWorkSheet.update_cells(cell_list)
			else:
				print("nothing to push")
	
	def __createSQLStatement(self,entity,startTime,endTime):
			sqlStatement = 'SELECT '
			
			for attribute in self.__selectAttributes[0: -1]:
				sqlStatement = ''.join([sqlStatement, attribute,' , '])
			#example output
			# 'SELECT created, state created FROM states WHERE entity_id = "media_player.kitchen_home" ORDER BY state_id DESC'
			sqlStatement =  ''.join([sqlStatement,self.__selectAttributes[-1]," FROM states WHERE state != 'unknown' AND entity_id = '", entity, "' AND created BETWEEN '", startTime.strftime("%Y-%m-%d %H:%M:%S"), "' AND '",  endTime.strftime("%Y-%m-%d %H:%M:%S"),"'  ORDER BY state_id ASC"])
			#print(sqlStatement)
			return sqlStatement
			
			
	'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	/if worksheet exists will return true
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
	def __checkSheetsCreated(self,entity):
		#output a list of all the sheets in a document
		listWorkSheets = self.__spreadSheet.worksheets()
		
		for workSheet in listWorkSheets:
			if(entity == workSheet.title):
				return True
		return False
	
	def __connectGoogle(self):
		scope = ['https://spreadsheets.google.com/feeds']

		credentials = ServiceAccountCredentials.from_json_keyfile_name('/share/googleDriveCredentials.json', scope)
		self.__gc = gspread.authorize(credentials)
		
	def __connectToDataBase(self):
		self.__conn = sqlite3.connect('/config/home-assistant_v2.db')
	'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	/will return the top most empty index
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''	
	def __getPositionLastActiveRow(self):
		#if the sheet exist but the top values not valid
		#return -1		
		if(self.__currentWorkSheet.cell(1,1).value == ''):
			return -1
			
		currentPosition = self.__currentWorkSheet.row_count
		
		#from the bottom most cell keep going up untill a values reached 
		while(self.__currentWorkSheet.cell(currentPosition,1).value == ''):
			currentPosition = currentPosition - 10
			#currentPosition can be below index of 2
			if(currentPosition <= 2):
				currentPosition = 2
				break
			#print(currentPosition)
		#once a value is reached move up by 1 untill no value is there
		#this is the bottom most empty index
		while(self.__currentWorkSheet.cell(currentPosition,1).value != ''):
			currentPosition = currentPosition + 1
			#print(currentPosition)
		#print(currentPosition)
		return currentPosition
	'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	/ fills the first row with the header information
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''	
	def __uploadHeader(self):
		print("uploading header")
		for i, attribute in enumerate(self.__selectAttributes):
			print(attribute)
			self.__currentWorkSheet.update_cell(1, i +1, attribute)
	'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	/ each spreadsheet has a limited amount
	/ of row so if the data your about to put
	/ in exceeds that you must add more rows.
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
	def _addExtraRows(self,currentPosition, lengthAddedRows):
		addingAmmount = 100
		if( (currentPosition + lengthAddedRows) >= self.__currentWorkSheet.row_count ):
			numberOfGroupsOfRowsToAdd = math.ceil( (float(currentPosition+ lengthAddedRows) - self.__currentWorkSheet.row_count) / addingAmmount)
			#print(numberOfGroupsOfRowsToAdd)
			self.__currentWorkSheet.add_rows(int(numberOfGroupsOfRowsToAdd * addingAmmount))
