# Adding parent directory to the PYTHONPATH
import sys, os
sys.path.insert(0,'..')
from utils.GlobalVariables import *
from utils.AwesomeLogger import Logger
import logging
from datetime import datetime


class BaseTrader(object):
	# Base class for creating trader agents
	# This is a very rough idea, it must be completed in the future
	def __init__(self, pair_name= 'UNSPECIFIED'):
		super(BaseTrader, self).__init__()

		# This is the name of the report folder, all reports including graphs, analysis, etc. will be saved under this name
		name = pair_name + "-" + str(datetime.now())[:-10].replace(":", "-")

		# Creating the report directory
		self.report_dir = f"../test_reports/Report-{name}"
		if not os.path.exists(self.report_dir):
			os.makedirs(self.report_dir)

		# Crearing logger
		logging_address = os.path.join(self.report_dir, 'Report.log')
		self.log = Logger(logger_name = 'AwesomeLogger', address = logging_address , mode='a',
							level = logging.DEBUG,
							console_level = logging.INFO,
							file_level = logging.DEBUG)

	def draw_graph(self):
		# This method must draw a graph based on the report of the trades
		pass

	def analyze_trades(self):
		# This method should analyze the trades and save them as a report
		# This report should use logging
		pass

	def save_trade_history(self):
		# This method saves the report created by the trader in a csv file
		# The file should be similar to the MT4 trade history
		pass


if __name__ == '__main__':
	import pandas as pd
	df = pd.read_csv('TestForBaseTrader.csv', index_col =0)

	def date_parser_1(date_as_str):
		# For the case index: 5/12/1993 0:00
		# There might be other cases so I named it date_parser_1
		return datetime.strptime(date_as_str, "%m/%d/%Y %H:%M")

	df['opening_time'].apply(date_parser_1)
	df['closing_time'].apply(date_parser_1)

	myBaseTrader = BaseTrader()
	myBaseTrader.report = df

	print (myBaseTrader.report)







