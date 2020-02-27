# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *

class Trade(object):
	# This class will be used in the traders to record the trades's information

	def __init__(self, main_pair, aux_pair):
		super(Trade, self).__init__()

	def set_opening_info(self, opening_time, main_open_price, aux_open_price, risk, balance):
		self.opening_time = opening_time
		self.main_open_price = main_open_price
		self.aux_open_price = aux_open_price
		self.risk = risk
		self.balance = balance

	def set_closing_info(self, closing_time, closing_price, closing_reason):
		self.closing_time = closing_time
		self.closing_price = closing_price
		self.closing_reason = closing_reason

	def evaluate(self):
		# Returns:
		# profit: as money
		# closing_balance
		# report as a dictionary of the required information
		# It should calculate the profit as well


		return profit, closing_balance, report

if __name__ == '__main__':
	1