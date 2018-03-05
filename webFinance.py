import sqlite3
import Finance
import pdfkit

from bottle import route , run, request, template, redirect


@route('/')
def homePage():
    return """
		<html>
		<head> {}
		</head>
		<body>
		<div class="container">

		<header><h1>Income Expense Tracker</h1></header>
		<nav>
		<ul>
		<br><a href="http://localhost:9999/addExpenseIncomeForm">Add your expense or income details</a></br>
		<br><a href="http://localhost:9999/reportFilterForm">Query your expense or income details</a></br>
		</ul>
		</nav>
		<footer>Finance 1.0</footer>
		</div>
		</body>
		</html>
		""".format(styleSheet)

@route('/addExpenseIncomeForm')
def addExpenseIncomeForm():
	fileContext = open("categoryList.txt", 'r')
	formContent = """
	<head> {}
	</head>
	<body>
	<div class="container">
	<header><h1>Log Income / Expense </h1></header>
	<form method="post" action="http://localhost:9999/addExpenseIncome">
	<p>
	<input type=radio name=transactionType value="Expense" checked>Expense
	<input type=radio name=transactionType value="Income" >Income
	<input type=radio name=transactionType value="Saving" >Savings<br>
	</p>
	<p>&#8377<tb><input type=text name=amount></p>
	<p><select name="category">
	""".format(styleSheet)
	
	for categoryEntry in fileContext:
		entry = categoryEntry.split(':')
		if(entry[1].rstrip()!= "ALL"):
			formContent = formContent + "<option value="'{}'">{}</option>".format(entry[1].rstrip(),entry[1].rstrip())
	fileContext.close
	
	formContent = formContent +	"""
    </select></p>
    
	<input type=date name=eventDate>
	<p><textarea name="description" rows='4' cols="50" >description</textarea></p>
	<p><input type=submit></p>
	
	<br><a href="http://localhost:9999/">Home Page</a></br>

	</form>
		<footer>Finance 1.0</footer>
		</div>
		</body>
		</html>
    """
	return formContent

@route('/addExpenseIncome',method='POST')
def addExpenseIncome():
	category = request.forms.get('category')
	eventDate = request.forms.get('eventDate')
	description = request.forms.get('description')
	transactionType = request.forms.get('transactionType')
	amount = request.forms.get('amount')
	Finance.Finance().addExpenseIncome(category,description,eventDate,transactionType,amount)
	redirect("http://localhost:9999/addExpenseIncomeForm")

@route('/reportFilterForm')
def reportFilterForm():
	fileContext = open("categoryList.txt", 'r')
	formContent = """
		<head> {}
		</head>
		<body>
		<div class="container">

		<header><h1>Income Expense Report Filters</h1></header>
	<form method="post" action="http://localhost:9999/Report">
	<br>
	<p><input type=radio name=transactionType value="Expense" checked>Expense
	<input type=radio name=transactionType value="Income" >Income
	<input type=radio name=transactionType value="Saving" >Saving
	<input type=radio name=transactionType value="ALL" >ALL
	</p>
	</br>
	Select category:<select name="category">
	""".format(styleSheet)
	
	for categoryEntry in fileContext:
		entry = categoryEntry.split(':')
		formContent = formContent + "<option value="'{}'">{}</option>".format(entry[1].rstrip(),entry[1].rstrip())
	fileContext.close
	
	formContent = formContent +	"""
    </select>
	
	From Date : <input type=date name=fromDate>
	To Date : <input type=date name=toDate>
	
	<input type=submit>
	<br/>
	<a href="http://localhost:9999/">Home Page</a>
	</p>
	</form>
	<footer>Finance 1.0</footer>
	</div>
	</body>
	</html>
    """
	return formContent

@route('/Report',method='POST')
def Report():
	total = 0
        output="""<style>
	table {border-collapse: collapse;width: 100%;}
	th, td {text-align: left;padding: 8px;}
	tr:nth-child(even){background-color: #f2f2f2}
	</style>
	<table border=1>
	<h1>Finance Report</h1>
	<tr><th>category</th><th>Description</th><th>Date</th><th>Transaction Type</th><th>Amount</th>
	</tr>"""
        tablerow="""<tr>
	<td>{}</td>
	<td>{}</td>
	<td>{}</td>
	<td>{}</td>
	<td>{}</td>
	
	</tr>"""
	categoryFilter = request.forms.get('category')
	fromDateFilter = request.forms.get('fromDate')
	toDateFilter = request.forms.get('toDate')
	transactionTypeFilter = request.forms.get('transactionType')

	for id,category,description,eventDate,transactionType,amount in Finance.Finance().Report(categoryFilter,transactionTypeFilter,fromDateFilter,toDateFilter):
		output += tablerow.format(category,description,eventDate,transactionType,amount)
		total = total + amount
	output+="</table>"
	output+="<br/><h2>Total {} : {}</h2> ".format(transactionTypeFilter,total)
	writeToFile(output)
	return output + """
	<br><a href="http://localhost:9999/downloadAsPdf">Download as pdf</a></br>
	<br><a href="http://localhost:9999/reportFilterForm">Back</a></br>
	<br><a href="http://localhost:9999/">Home Page</a></br>
	"""
 
def writeToFile(content):
	fileWrite = open("Report.html",'w')
	fileWrite.write(content)
	fileWrite.close
	
	
	
@route('/downloadAsPdf')
def download():
	path_wkthmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
	config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
	pdfkit.from_url('Report.html', 'out.pdf', configuration=config)
	redirect("http://localhost:9999/")
	
	

styleSheet = """
<style>
div.container {
    width: 100%;
    border: 1px solid gray;
}

header, footer {
    padding: 1em;
    color: white;
    background-color: black;
    clear: left;
    text-align: center;
}

nav {
    float: left;
    max-width: 160px;
    margin: 0;
    padding: 1em;
}

nav ul {
    list-style-type: none;
    padding: 0;
}
   
nav ul a {
    text-decoration: none;
}

article {
    margin-left: 170px;
    border-left: 1px solid gray;
    padding: 1em;
    overflow: hidden;
}
</style>
"""
	
run(host='localhost',port=9999,debug=True)

