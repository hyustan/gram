# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *
from trader.BaseTrader import BaseTrader


class RowTrader(BaseTrader):

	# The trade's method of this class will iterate over rows
	# it predicts one row at a time

	def __init__(self, main_pair, aux_pair, features, risk = 2, initial_money = 10000):
		super(TestTrader, self).__init__()
		self.main_pair = main_pair
		self.aux_pair = aux_pair
		self.features = features
		self.risk = risk
		self.initial_money = initial_money

	def trade(self, , dm = 'Decision Model'):
		pass

if __name__ == '__main__':
