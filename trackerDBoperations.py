from dbToDo import dbOperations
import datetime

class TrackerDbOperations(object):

	## global variables
	connection = None
	tableName = 'Tracker'
	dataBaseName = 'TrackerDataBase.db'
	dboperations = None
		
	#Common DB Queries
	CREATE_TABLE_QUERY = "CREATE TABLE {} (id int,createDate text,modifiedDate text , targetDate text, plan text)".format(tableName)
	SELECT_QUERY = "SELECT * from Tracker"
	
	def __init__(self):
		self.dboperations = dbOperations()
		self.connection = self.dboperations.connectToDB(self.dataBaseName)
		cursor = self.dboperations.getCursor(self.connection)
		if ( self.dboperations.isSchemaAvailable(self.connection,self.tableName) == 0):
			self.dboperations.executeQuery(cursor,self.CREATE_TABLE_QUERY)
			
		
	def addPlan(self,targetTimeStamp,plan):
		self.connection = self.dboperations.connectToDB(self.dataBaseName)
		cursor = self.dboperations.getCursor(self.connection)
		
		resultSet = self.listPlan()
		if len(resultSet) <= 0:
			ID = 1
		if len(resultSet) > 0:
			FIND_MAXID_QUERY="select max(id) from {}".format(self.tableName,id)
			rows = self.dboperations.executeQuery(cursor,FIND_MAXID_QUERY)
			row = rows.fetchone()
			ID = int(row[0]) + 1
		createDate = "'" + str(datetime.datetime.now()) +"'"
		modifiedDate =  "'" + str(datetime.datetime.now())+"'"
		targetDate =  "'" + targetTimeStamp +"'" 
		plan = "'" + plan +"'" 
		cursor = self.dboperations.getCursor(self.connection)
		ADD_PLAN_QUERY = "INSERT INTO {}(id ,createDate,modifiedDate,targetDate,plan) VALUES({},{},{},{},{})".format(self.tableName,ID,createDate,modifiedDate,targetDate,plan)
		c = self.dboperations.executeQuery(cursor,ADD_PLAN_QUERY)
		self.connection.commit()
		
	def listPlan(self):
		self.connection = self.dboperations.connectToDB(self.dataBaseName)
		cursor = self.dboperations.getCursor(self.connection)
		cursor = self.dboperations.executeQuery(cursor,self.SELECT_QUERY)
		resultSet = cursor.fetchall()
		return resultSet

	def deletePlan(self,id):
		self.connection = self.dboperations.connectToDB(self.dataBaseName)
		cursor = self.dboperations.getCursor(self.connection)
		DELETE_QUERY="DELETE from {} where id={}".format(self.tableName,id)
		cursor = self.dboperations.executeQuery(cursor,DELETE_QUERY)
		self.connection.commit()

	def updatePlan(self,planDateTime,plan,id):
		self.connection = self.dboperations.connectToDB(self.dataBaseName)
		cursor = self.dboperations.getCursor(self.connection)
		modifiedDate = str(datetime.datetime.now())
		targetDate = planDateTime
		UPDATE_QUERY= "UPDATE {} SET targetDate='{}', modifiedDate='{}', plan='{}' WHERE id={}".format(self.tableName,targetDate,modifiedDate,plan,id)
		cursor = self.dboperations.executeQuery(cursor,UPDATE_QUERY)
		self.connection.commit()

	def deleteExpiredplan(self):
		dateFormat = '%Y-%m-%d %H:%M:%S'
		self.connection = self.dboperations.connectToDB(self.dataBaseName)
		cursor = self.dboperations.getCursor(self.connection)
		cursor = self.dboperations.executeQuery(cursor,self.SELECT_QUERY)
		resultSet = cursor.fetchall()
		for row in resultSet:
			id = row[0]
			targetTimeStamp = datetime.datetime.strptime(row[3], dateFormat)
			currentTimeStamp = datetime.datetime.now()
			if(targetTimeStamp < currentTimeStamp):
				DELETE_QUERY="DELETE from {} where id={}".format(self.tableName,id)
				cursor = self.dboperations.executeQuery(cursor,DELETE_QUERY)
				self.connection.commit()
		return "deleted all Expired plan"

# Functionality to be implemented later				
	def sendReminder(self):
		#send an email as reminder 
		pass
