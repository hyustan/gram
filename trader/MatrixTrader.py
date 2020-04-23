# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from data.FXDataLoader import Pair
from trader.BaseTrader import BaseTrader
from trader.Trade import Trade
from indicators.ATR import ATR
from decision_models.CoinToss import CoinToss

class MatrixTrader(BaseTrader):

	# The trade's method of this class will iterate over rows
	# it predicts one row at a time

	def __init__(self,main_pair, aux_pair, balance = 10000, risk = 0.02, spread = 3, should_trailing_stop = True, timeframe = '1D'):

		super(MatrixTrader, self).__init__(main_pair.name)

		self.main_pair = main_pair
		self.aux_pair = aux_pair
		self.balance = balance
		self.risk = risk
		self.spread = spread/10000 if not 'JPY' in self.main_pair.name else spread/100
		self.should_trailing_stop = should_trailing_stop

		if timeframe == '1D':
			self.df = main_pair.get_1D()
		elif timeframe == '4H':
			self.df = main_pair.get_4H()
		elif timeframe == '1H':
			self.df = main_pair.get_1H()

		self.atr = ATR(14).calculate(self.df)
		
	def simulate(self, signals, should_draw = True, should_analyze = True, should_save = True):
		# Report should be dataframe of all trades consisiting the trades' reports
		# Trades' report is a dictionary. You may find it in the Trade class in the same folder
		# total_profit is the sum of all trades' profits

		# Initializing the the required parameters
		in_trade = False
		trade_list = []
		total_profits = 0
		balance = self.balance

		# iterating over indices
		for index, next_index in zip(signals.index[:-1], signals.index[1:]):
			
			# Knowing the signal at the current time
			signal = signals[index]

			# check if we have an open trade
			if in_trade:
				
				# See if we have encountered an opposite signal
				opposite_signal = trade.trade_type * signal < 0

				# Close the trade with opposite signal
				if opposite_signal:

					in_trade = False

					# Check if we have closed the trade_1 yet or not
					if trade.trade_1_open:
						trade.set_closing_info_1(closing_time = index,
												main_closing_price = row[CLOSE],
									 			aux_closing_price = row[CLOSE],
									 			closing_reason = 'opposite_signal')
					# Closing the trade_2
					trade.set_closing_info_2(closing_time = index,
											main_closing_price = row[CLOSE],
								 			aux_closing_price = row[CLOSE],
								 			closing_reason = 'opposite_signal')

					profit, balance = trade.evaluate()
					trade_list.append(trade.get_report())
					total_profits += profit

					# check pelle                        
					if trade.trade_type is LONG and row[CLOSE] > trade.pelle_price:
						trade.Stoploss_trade2 = trade.pelle_price-row['ATR']
						trade.pelle_price = trade.pelle_price+row['ATR']
					if trade.trade_type is SHORT and row[CLOSE] < trade.pelle_price:
						trade.stop_loss2 = trade.pelle_price+row['ATR']
						trade.pelle_price = trade.pelle_price-row['ATR']
				else:

					for time, moment_row in self.main_pair.get_5M().loc[index:next_index].iterrows():
						
						# check stoplosses
						cross_sl1 = ((trade.trade_type is SHORT and moment_row[CLOSE] > trade.stop_loss1) or
							    (trade.trade_type is LONG and moment_row[CLOSE] < trade.stop_loss1))

						cross_sl2 = ((trade.trade_type is SHORT and moment_row[CLOSE] > trade.stop_loss2) or
							    (trade.trade_type is LONG and moment_row[CLOSE] < trade.stop_loss2))

						if cross_sl2:
							in_trade = False
							if trade_1_open:
								trade.set_closing_info_1(closing_time = time,
											 main_closing_price = moment_row[CLOSE],
											 aux_closing_price = moment_row[CLOSE],
											 closing_reason = 'stop_loss')

							trade.set_closing_info_2(closing_time = time,
											 main_closing_price = moment_row[CLOSE],
											 aux_closing_price = moment_row[CLOSE],
											 closing_reason = 'stop_loss')
							
							profit, balance = trade.evaluate()
							trade_list.append(trade.get_report())
							total_profits += profit
							break
							    
						if cross_sl1:
							trade.set_closing_info_1(closing_time = time,
											 main_closing_price = moment_row[CLOSE],
											 aux_closing_price = moment_row[CLOSE],
											 closing_reason = 'stop_loss')
						# check take profit
						crossTP = ((trade.trade_type is SHORT and moment_row[CLOSE] < trade.take_profit) or
							   (trade.trade_type is LONG and moment_row[CLOSE] > trade.take_profit))

						if crossTP:
							trade.set_closing_info_1(closing_time = time,
											 main_closing_price = moment_row[CLOSE],
											 aux_closing_price = moment_row[CLOSE],
											 closing_reason = 'take_profit')
			if not in_trade:
				if row['ATR'] != row['ATR']:
					continue
				trade_type = signal
				in_trade = True
				trade = Trade(self.main_pair_name, self.aux_pair_name)
				trade.set_opening_info(opening_time = next_index,
						 main_open_price = self.df[OPEN][next_index],
						 aux_open_price = self.df[OPEN][next_index],
						 trade_type = trade_type,
						 balance = balance,
						 ATR = row['ATR'],
						 risk = self.risk,
						 stop_loss1=  self.df[OPEN][next_index] - trade_type * 1.5 * row['ATR'],
						 stop_loss2 = self.df[OPEN][next_index] - trade_type * 1.5 * row['ATR'],
						 pelle_price = self.df[OPEN][next_index] + trade_type * row['ATR'],
						 take_profit = self.df[OPEN][next_index] + trade_type * row['ATR'])

		self.report = pd.DataFrame(trade_list)

		if should_draw: self.draw_graph()
		if should_analyze: self.analyze_trades()
		if should_save: self.save_trade_history()

		return total_profits
		



if __name__ == '__main__':
	# GBPUSD_data = Pair(GBPUSD)
	# # Dataframe for test
	# dfall = GBPUSD_data.get_1D()
	# df = dfall[-500:-200]# the five minutes time frame does not cover the 1 D range!!!!
	# df.index = df.index + timedelta(hours=13)# I am guessing we are not going to trade at 00:00:00 every day
	# atr = ATR(14)
	# df['ATR'] = atr.calculate(df)
	# df['signal'] = -1
	# df_moment = GBPUSD_data.get_5M()
	# matrix_trader = MatrixTrader('GBPUSD','GBPUSD',df,df_moment,1000)
	# report = matrix_trader.simulate()
	# myBaseTrader = BaseTrader()
	# myBaseTrader.report = report
	# myBaseTrader.draw_graph()
	# myBaseTrader.save_trade_history()
	# myBaseTrader.analyze_trades()


	GBPUSD_data = Pair(GBPUSD)
<<<<<<< HEAD
	# Dataframe for test
	dfall = GBPUSD_data.get_1D()
	df = dfall.loc[dfall.index[-500:-200]]# the five minutes time frame does not cover the 1 D range!!!!
	df.index = df.index + timedelta(hours=13)# I am guessing we are not going to trade at 00:00:00 every day
	atr = ATR(14)
	df['ATR'] = atr.calculate(df)
	df['signal'] = -1
	df_moment = GBPUSD_data.get_5M()
	matrix_trader = MatrixTrader('GBPUSD','GBPUSD',df,df_moment,1000)
	trade_log = matrix_trader.simulate()
	myBaseTrader = BaseTrader()
	myBaseTrader.report = trade_log
	myBaseTrader.draw_graph()
	myBaseTrader.save_trade_history()
	myBaseTrader.analyze_trades()
=======
	matrix_trader = MatrixTrader(GBPUSD_data, GBPUSD_data, timeframe = '1D')
	dm = CoinToss()
	
	features = pd.DataFrame(np.random.rand(len(GBPUSD_data.get_1D()), 5))
	signals = pd.Series(dm.decide(features), features.index)

	matrix_trader.simulate(signals)




>>>>>>> d9195bc9a905b705f6b98be54f3afd6f0925dce3
