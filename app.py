#import modules
from flask import Flask, render_template, request, flash, url_for, redirect
import mysql.connector
import pygal
from pygal.style import LightenStyle

#create a flask app object and set app variables
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRECT_KEY"] = 'your secret key'
app.secret_key = 'your secret key'

#create a connection object to the classicmodels database
#def get_db_connection():
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    port="6603",
    database="classicmodels"
)

cursor = mydb.cursor(dictionary=True)

#function to check if the form is filled out
def formCheck(reportType, year):
    if not reportType:
        flash("Error: You must choose a report option")
        return False
    
    if not year:
        flash("Error: You must select a year")
        return False
    
    return True

#function to create graph
def createGraph(title, labels, valuesTitle, values):
    #styling the graph
    style = LightenStyle('#8AAC93')
    style.background = 'transparent'
    style.plot_background = '#C2DFCB'

    #creating graph object with variables passed to function
    chart_title = title
    chart_object = pygal.Bar(x_label_rotation=45, height=400, style=style)
    chart_object.title = chart_title
    chart_object.x_labels = labels
    chart_object.add(valuesTitle, values)

    return chart_object.render_data_uri()

#index route
@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        reportSelection = request.form.get("selection")

        if not reportSelection:
            flash("Error: Must select a report option")
            return redirect(url_for("index"))

        if reportSelection == "products":
            return redirect(url_for("products"))
        elif reportSelection == "customers":
            return redirect(url_for("customers"))
        elif reportSelection == "employees":
            return redirect(url_for("employees"))
    
    return render_template('index.html')

#products route
@app.route('/product-reports', methods=['GET', 'POST'])
def products():
    years = []
    query=""
    monthlyResults = None
    productLineResults = None
    productResults = None
    chart = None

    #get years for form
    year_query= 'SELECT DISTINCT YEAR(orderDate) FROM orders;'
    cursor.execute(year_query)
    years = cursor.fetchall()

    if request.method == 'POST':

        #get the form values
        reportType= request.form.get("reportType")
        year = request.form.get("year")

        #check to make sure the form is filled out
        if not formCheck(reportType, year):
            return redirect(url_for("products"))
        
        #display results
        if reportType == "monthly":
            query = "SELECT * FROM monthlyOrderTotals WHERE orderYear = %s;"
            cursor.execute(query, (year,))
            monthlyResults = cursor.fetchall()

            #create graph from results
            months = []
            totals = []
            for month in monthlyResults:
                months.append(month['orderMonth'])
                totals.append(month['totalOrderValue'])

            chart = createGraph(f"Year {year}: Product Sales", months, "Sales", totals)

        elif reportType == "byProductLine":
            query = "SELECT * FROM totalsByProductLine WHERE orderYear = %s;"
            cursor.execute(query, (year,))
            productLineResults = cursor.fetchall()

            #create graph from results
            products = []
            totals = []
            for product in productLineResults:
                products.append(product['productLine'])
                totals.append(product['totalOrderValue'])

            chart = createGraph(f"Year {year}: Product Line Sales", products, "Sales", totals)

        elif reportType == "byProducts":
            query = "SELECT * FROM totalsByProduct WHERE orderYear = %s;"
            cursor.execute(query, (year,))
            productResults = cursor.fetchall()

            #create graph using top ten results
            products = []
            totals = []
            count = 0
            for product in productResults:
                products.append(product['productName'])
                totals.append(product['totalOrderValue'])
                #making sure only the top 10 customers are added to the list
                count += 1
                if count == 10:
                    break

            chart = createGraph(f"Year {year}: Top 10 Product Sales", products, "Sales", totals)            

    return render_template('products.html', years = years, monthlyResults = monthlyResults, productLineResults = productLineResults, productResults = productResults, chart = chart)

#customers route
@app.route('/customers-reports', methods=['GET', 'POST'])
def customers():
    years = []
    query=""
    ordersResult = None
    paymentsResult = None
    chart = None

    #get years for form
    year_query= 'SELECT DISTINCT YEAR(orderDate) FROM orders;'
    cursor.execute(year_query)
    years = cursor.fetchall()

    if request.method == 'POST':
        #get the form values
        reportType= request.form.get("reportType")
        year = request.form.get("year")

        #check to make sure the form is filled out
        if not formCheck(reportType, year):
            return redirect(url_for("customers"))
        
        #display results
        if reportType == "orders":
            query = "SELECT * FROM customerOrderTotals WHERE orderYear = %s;"
            cursor.execute(query, (year,))
            ordersResult = cursor.fetchall()

            #create graph with top 10 results
            totals = []
            customers = []
            count = 0 
            for order in ordersResult:
                totals.append(order['totalOrder'])
                customers.append(order['customerName'])
                #making sure only the top 10 customers are added to the list
                count += 1
                if count == 10:
                    break

            chart = createGraph(f"Year {year}: Top 10 Customer Orders", customers, "Order Totals", totals)
            

        elif reportType == "payments":
            query = "SELECT * FROM customerPayments WHERE paymentYear = %s;"
            cursor.execute(query, (year,))
            paymentsResult = cursor.fetchall()

            #creat graph with top 10 results
            payments = []
            customers = []
            count = 0 
            for customer in paymentsResult:
                payments.append(customer['totalPayment'])
                customers.append(customer['customerName'])
                #making sure only the top 10 customers are added to the list
                count += 1
                if count == 10:
                    break

            chart = createGraph(f"Year {year}: Top 10 Customer Payments", customers, "Payments", payments)           

    return render_template('customers.html', years = years, ordersResult = ordersResult, paymentsResult = paymentsResult, chart = chart)

#employees route
@app.route('/employees-reports', methods=['GET', 'POST'])
def employees():
    years = []
    query=""
    totalOrdersResult = None
    numOfOrdersResult = None
    chart = None


    #get years for form
    year_query= 'SELECT DISTINCT YEAR(orderDate) FROM orders;'
    cursor.execute(year_query)
    years = cursor.fetchall()

    if request.method == 'POST':

        #get the form values
        reportType= request.form.get("reportType")
        year = request.form.get("year")

        #check to make sure the form is filled out
        if not formCheck(reportType, year):
            return redirect(url_for("employees"))
        
        if reportType == "orders":
            query = "SELECT * FROM employeeOrderTotals WHERE orderYear = %s;"
            cursor.execute(query, (year,))
            totalOrdersResult = cursor.fetchall()

            #create graph with results
            totals = []
            employees = []
            for employee in totalOrdersResult:
                totals.append(employee['totalOrderValue'])
                employees.append(employee['employeeName'])

            chart = createGraph(f"Year {year}: Employee Order Report", employees, "Totals", totals)

        elif reportType == "numOfOrders":
            query = "SELECT * FROM employeeNumOfOrders WHERE orderYear = %s;"
            cursor.execute(query, (year,))
            numOfOrdersResult = cursor.fetchall()

            #create graph with results
            orders = []
            employees = []
            for employee in numOfOrdersResult:
                orders.append(employee['totalOrders'])
                employees.append(employee['employeeName'])

            chart = createGraph(f"Year {year}: Number of Orders by Employee", employees, "Orders", orders)

    return render_template('employees.html', years = years, totalOrdersResult = totalOrdersResult, numOfOrdersResult = numOfOrdersResult, chart = chart)

app.run(port=5008, debug=True)