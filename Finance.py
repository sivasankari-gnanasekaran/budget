from DBOperations import dbOperations
import datetime

# ToDos -
#1)try to split income and exp table. Keep category in a separate table rather than reading from file
#2)Add button to bring the expenseIncome adding experience
#3)Render the category in a drop down - done

class Finance(object):
    ## global variables
    connection = None
    tableName = 'finance'
    dataBaseName = 'Budget.db'
    dboperations = None
		
    #Common DB Queries
    CREATE_TABLE_QUERY = """CREATE TABLE {} (id int,category text,description text , eventDate text,
    transactionType text, amount int)""".format(tableName)
    
   
    def __init__(self):
	self.dboperations = dbOperations()
        cursor = self.getCursor()
	if ( self.dboperations.isSchemaAvailable(self.connection,self.tableName) == 0):
            self.dboperations.executeQuery(cursor,self.CREATE_TABLE_QUERY)
        pass

    def addExpenseIncome(self,category,description,eventDate,transactionType,amount):
		cursor = self.getCursor()
		ID = self.incrementID()
		cursor = self.getCursor()
		quote = "'"
		category = quote + category + quote
		description = quote + description + quote
		eventDate = quote + eventDate + quote
		transactionType = quote + transactionType + quote
		ADD_QUERY = """INSERT INTO {}(id ,category,description,
		eventDate,transactionType,amount) VALUES({},{},{},{},{},{})""".format(self.tableName,ID,category,description,eventDate,transactionType,amount)
		c = self.dboperations.executeQuery(cursor,ADD_QUERY)
		self.connection.commit()
        

    def listAll(self,query):
        cursor = self.getCursor()
        cursor = self.dboperations.executeQuery(cursor,query)
	resultSet = cursor.fetchall()
    	return resultSet

    def reportQuery(self,query):
        cursor = self.getCursor()
        cursor = self.dboperations.executeQuery(cursor,query)
        return cursor.fetchall()

    def incrementID(self):
        cursor = self.getCursor()
        SELECT_ALL = "SELECT * from finance"
        resultSet = self.listAll(SELECT_ALL)
	if len(resultSet) <= 0:
            ID = 1
	if len(resultSet) > 0:
            FIND_MAXID_QUERY="select max(id) from {}".format(self.tableName,id)
            rows = self.dboperations.executeQuery(cursor,FIND_MAXID_QUERY)
            row = rows.fetchone()
            ID = int(row[0]) + 1
        return ID

    
    def Report(self,category,transactionType,fromDate,toDate):
		quote = "'"
		ALL = "'ALL'"
		category = quote + category + quote
		fromDate = quote + fromDate + quote
		toDate = quote + toDate + quote
		transactionType = quote + transactionType + quote
		if (transactionType == ALL and category == ALL):
			SELECT_BY_TYPE_QUERY = "SELECT * from finance where eventDate > {} AND eventDate < {} ORDER BY transactionType, eventDate".format(fromDate,toDate)
		elif category == ALL:
			SELECT_BY_TYPE_QUERY = "SELECT * from finance where transactionType={} AND eventDate > {} AND eventDate < {} ORDER BY category".format(transactionType,fromDate,toDate)
		elif transactionType == ALL:
			SELECT_BY_TYPE_QUERY = "SELECT * from finance where category={} AND eventDate > {} AND eventDate < {} ORDER BY transactionType".format(transactionType,category,fromDate,toDate)
		else:
			SELECT_BY_TYPE_QUERY = "SELECT * from finance where transactionType={} AND category={} AND eventDate > {} AND eventDate < {}".format(transactionType,category,fromDate,toDate)
		return self.reportQuery(SELECT_BY_TYPE_QUERY)
		

    def mailMeReport(self):
        pass

    def getCursor(self):
        self.connection = self.dboperations.connectToDB(self.dataBaseName)
        cursor = self.dboperations.getCursor(self.connection)
        return cursor
    
#------------------------------------------------------------------------------------------------------    
#obj = Finance()
#obj.addExpenseIncome("'transport'","'went to work'","2016-08-01",1)
# 1 - exp
# 2 - income
# 3 - savings
#for id,category,description,eventDate,transactionType,amount in obj.Report("Rent/Mortgage",2,"2016-08-01" , "2016-08-31"):
#	print str(id)+","+category+","+description+","+eventDate+","+str(transactionType) +","+str(amount)
