from StockClasses import Investor, Stock, Bond
import unittest

class testInvestor (unittest.TestCase):
    def test_investor(self):
        investorName = Investor(1,'Bob Smith','123,Denver,Co','7201231234')
        name = investorName.name
        self.assertEqual('Bob Smith' , name)
    def testStock (self):
        stock1 = Stock( 1, 'GOOGL', 25, 772.88, 941.53, '2017/8/1'  )
        stock_test = stock1.ProfitLoss
        self.assertEqual( 4216.25, stock_test)
    def testBond (self):
        bond1 = Bond(  1, 'GT2:GOV', 200, 100.02, 100.05, '2018/5/12', 1.35, 1.38  )
        bond_test = bond1.ProfitLoss
        self.assertEqual( 6.0 , bond_test )

if __name__ == '__main__':
    unittest.main()