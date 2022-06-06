"""
    Author        : Sravya Motepalli

    Date created  : 06/01/2022

    Functionality : PORTFOLIO PROGRAMMING ASSIGNMENT - IMPROVING THE STOCK PROBLEM WITH ADDITIONAL FUNCTIONALITY

"""
# Import required libraries
import sqlite3
import plotly.express as px
import csv
import pandas as pd
import json
from datetime import datetime

# Establishing Database Connection
from pandas import read_csv
dbPath = r'C:\Users\shrav\Documents\Python_files_classes\Stocks_json.db'

try:
    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()

except:
    print('failed to connect to database')

# Creating a dataset using pandas from json file
filepath = r'C:\Users\shrav\Documents\Python_files_classes\AllStocks.json'
with open(filepath) as json_file:
    dataset = json.load(json_file)

# Creating a class for stocks and to calculate profit or loss
class Stock:
    def __init__(self, ID, symbol, quantity, purchasePrice, currentPrice, purchaseDate):
        self.ID = ID
        self.symbol = symbol
        self.quantity = quantity
        self.purchasePrice = purchasePrice
        self.currentPrice = currentPrice
        self.purchaseDate = purchaseDate
        self.ShareGainLoss = round((self.currentPrice - self.purchasePrice), 2)
        self.ProfitLoss = round((self.ShareGainLoss * self.quantity), 2)

# Creating Class for creating database table and exporting data into it
class create_data:
    def __init__(self, symbol, date, value):
        self.symbol = symbol
        self.date = date
        self.value = value

    def create_table(self):
        stock_table = " CREATE TABLE IF NOT EXISTS " + self.symbol
        stock_table = stock_table + "( Date date PRIMARY KEY," + self.symbol + " real NOT NULL ) "
        cursor.execute(stock_table)

    def insert_data(self):
        insert_data = 'INSERT or IGNORE INTO ' + self.symbol + " VALUES ('"
        insert_data = insert_data + str(self.date)
        insert_data = insert_data + " ',' " + str(self.value) + "' );"
        cursor.execute(insert_data)

#Reading CSV file and creating symbol list
workspace = r'C:\Users\shrav\PycharmProjects\pythonProject'
Stock_File = workspace + '\\' + 'Lesson6_Data_Stocks.csv'
Read_Stocks = open(Stock_File, 'r')
data = read_csv("Lesson6_Data_Stocks.csv")
stockSymbols = data['SYMBOL'].tolist()

# looping to remove '-' in the list
for symbol in stockSymbols:
    if symbol == "RDS-A":
        index = stockSymbols.index('RDS-A')
        stockSymbols.remove("RDS-A")
        stockSymbols.insert(index, 'RDSA')

#Reading CSV file and creating dictinory list
stock_dict = {}
with open('Lesson6_Data_Stocks.csv', mode='r') as inp:
    reader = csv.reader(inp)
    next(reader)
    stock_dict = {rows[0]:int(rows[1]) for rows in reader}
    stock_dict["RDSA"] = stock_dict.pop("RDS-A")


# Create a loop to create individual stock tables
for data in dataset:
    try:
        stockDate = datetime.strptime(data['Date'], '%d-%b-%y')
    except ValueError:
        print('Date format of this stock is not correct')

#writing a if else condition to make sure file reads correctly
    if data['Symbol'] == 'RDS-A':
        stockVal = round(data['Close'] * stock_dict['RDSA'], 2)
        newStock = create_data('RDSA', stockDate, stockVal)
        newStock.create_table()
        newStock.insert_data()
    else:
        stockVal = round(data['Close'] * stock_dict[data['Symbol']], 2)
        newStock = create_data(data['Symbol'], stockDate, stockVal)
        newStock.create_table()
        newStock.insert_data()

# Merge all the individual stocks into single dataframe
select_dates = "SELECT Date FROM AIG"
df_all_stocks = pd.read_sql_query(select_dates, connection)
for stock in stockSymbols:
    select_table = "SELECT * from " + stock
    df_name = stock + '_df'
    df_name = pd.read_sql_query(select_table, connection)
    df_all_stocks = pd.merge(df_all_stocks, df_name, how='left', on=["Date"])

# Plot the graph using Plotly
fig = px.line(df_all_stocks, x="Date", y=df_all_stocks.columns,
              hover_data={"Date": "|%Y,%m,%d"},
              title=' Stock Portfolio')
fig.update_xaxes(dtick="M1", tickformat="%b\n%Y")
fig.show()

# Commit and Close Database
connection.commit()
connection.close()