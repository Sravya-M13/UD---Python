"""
    Author        : Sravya Motepalli

    Date created  : 06/01/2022

    Functionality : PORTFOLIO PROGRAMMING ASSIGNMENT - Classes for Inverstor, Stocks and Bonds

"""
#Importing stocks from main file
from PortfolioAssignment import Stock

# creating Investor class
class Investor:
    def __init__(self, investorID, name, address, phoneNumber):
        self.name = name
        self.investorID = investorID
        self.address = address
        self.phoneNumber = phoneNumber
        self.stocks = []
        self.bonds = []

    def investorStock(self, ID, symbol, quantity, purchasePrice, currentPrice, purchaseDate):
        self.stocks.append(Stock(ID, symbol, quantity, purchasePrice, currentPrice, purchaseDate))

    def investorBond(self, ID, symbol, quantity, purchasePrice, currentPrice, purchaseDate, Yield, coupon):
        self.bonds.append(Bond(ID, symbol, quantity, purchasePrice, currentPrice, purchaseDate, Yield, coupon))

    def investor_portfolio(self):
        print("\t   Stock Ownership for" + " " + self.name)
        print("-" * 55)
        print("Stock" + "\t" + "Share#" + "\t" + "Earnings/Loss" + "\t" + "Yearly Earning/Loss")
        for i in self.stocks:
            print(i.Stocks_Output())
        print(
            '\n' + "Bond" + "\t" + "Bond#" + "\t" + "Earnings/Loss" + "\t" + "Yearly Earning/Loss" + "\t" + "Yield" + "\t" + "coupon")
        for i in self.bonds:
            print(i.Bonds_output())

# Creating a class for bonds and to calculate profit or loss
class Bond(Stock):
    def __init__(self, ID, symbol, quantity, purchasePrice, currentPrice, purchaseDate, Yield, coupon):
        super().__init__(ID, symbol, quantity, purchasePrice, currentPrice, purchaseDate)
        self.Yield = Yield
        self.coupon = coupon
        self.BondGainLoss = round((self.currentPrice - self.purchasePrice), 2)
        self.ProfitLoss = round((self.BondGainLoss * self.quantity), 2)
