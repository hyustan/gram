# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *
from trader.BaseTrader import BaseTrader


class RowTrader(BaseTrader):

	# The trade's method of this class will iterate over rows
	# it predicts one row at a time

	def __init__(self, main_pair, aux_pair, feature_generator, risk = 2, initial_money = 10000):
		super(TestTrader, self).__init__()
		self.main_pair = main_pair
		self.aux_pair = aux_pair
		self.features = features
		self.risk = risk
		self.initial_money = initial_money

	def simulate(self, dm = 'Decision Model'):
		# Report should be dataframe of all trades consisiting the trades' reports
		# Trades' report is a dictionary. You may find it in the Trade class in the same folder
		# total_profit is the sum of all trades' profits

		
		self.report = None
		self.total_profit = None
		return total_profit, report

if __name__ == '__main__':
