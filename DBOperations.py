import sqlite3
import datetime
class dbOperations(object):

#global variables
	connection = None
	cursor = None
	
	def __init__(self):
		pass

	def isSchemaAvailable(self,connection,tableName):
		sql = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{}'".format(tableName)
		cursor = self.getCursor(connection)
		result = cursor.execute(sql).fetchone()
		return result[0]

	def connectToDB(self,dbName='dataBase.db'):
		connection = sqlite3.connect(dbName)
		return connection

	def getCursor(self,connection):		
		c = connection.cursor()
		return c

	def executeQuery(self,cursor,sql):
		print sql
		return cursor.execute(sql)

	def closeConnection(self,connection):
		connection.close
		
