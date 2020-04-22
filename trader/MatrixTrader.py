# Adding parent directory to the PYTHONPATH
import sys
import gc
sys.path.insert(0,'..')
import numpy as np
import pandas as pd
from utils.GlobalVariables import *
import BaseTrader
from Trade import Trade
from data.FXDataLoader import Pair
from indicators.ATR import ATR
from datetime import datetime, timedelta
from BaseTrader import BaseTrader

class MatrixTrader():

	# The trade's method of this class will iterate over rows
	# it predicts one row at a time

	def __init__(self,main_pair_name, aux_pair_name,df,df_moment,balance,risk = 0.03):
		self.main_pair_name = main_pair_name
		self.aux_pair_name = aux_pair_name
		self.df = df
		self.df_moment = df_moment
		self.balance = balance
		self.risk = risk
		
	def simulate(self):
		# Report should be dataframe of all trades consisiting the trades' reports
		# Trades' report is a dictionary. You may find it in the Trade class in the same folder
		# total_profit is the sum of all trades' profits

		# Iterate over rows
		in_trade = False
		trade_list = []
		balance = self.balance
		for index,next_index in zip(df.index[:-1],df.index[1:]):
			row = df.loc[index]
			# check opposit signal
			if in_trade:
				negativeSignal = ((trade.trade_type is SHORT and row['signal'] is 1) or
						  (trade.trade_type is LONG and row['signal'] is -1))
				if negativeSignal:
					in_trade = False
					if main_closing_price_1 not in trade:
						trade.set_closing_info_1(closing_time = index, main_closing_price = row[CLOSE],
									 aux_closing_price = row[CLOSE], closing_reason = 'opposit signal')
					trade.set_closing_info_2(closing_time = index, main_closing_price = row[CLOSE],
								 aux_closing_price = row[CLOSE], closing_reason = 'opposit signal')

					trade.evaluate()
					trade_report = trade.get_report()
					balance = trade.closing_balance
					trade_list.append(trade_report)
					# check pelle                        
					if trade.trade_type is LONG and row[CLOSE] > trade.Pelleprice:
						trade.Stoploss_trade2 = trade.Pelleprice-row['ATR']
						trade.Pelleprice = trade.Pelleprice+row['ATR']
					if trade.trade_type is SHORT and row[CLOSE] < trade.Pelleprice:
						trade.stop_loss2 = trade.Pelleprice+row['ATR']
						trade.Pelleprice = trade.Pelleprice-row['ATR']
				else:

					for time,moment_row in df_moment.loc[index:next_index].iterrows():
						# check stoploss
						crossSL1 = ((trade.trade_type is SHORT and moment_row[CLOSE] > trade.stop_loss1) or
							    (trade.trade_type is LONG and moment_row[CLOSE] < trade.stop_loss1))

						crossSL2 = ((trade.trade_type is SHORT and moment_row[CLOSE] > trade.stop_loss2) or
							    (trade.trade_type is LONG and moment_row[CLOSE] < trade.stop_loss2))

						if crossSL2:
							in_trade = False
							if not hasattr(trade,'close_trade1'):
								trade.set_closing_info_1(closing_time = time,
											 main_closing_price = moment_row[CLOSE],
											 aux_closing_price = moment_row[CLOSE],
											 closing_reason = 'stop loss')

							trade.set_closing_info_2(closing_time = time,
											 main_closing_price = moment_row[CLOSE],
											 aux_closing_price = moment_row[CLOSE],
											 closing_reason = 'stop loss')
							trade.evaluate()
							trade_report = trade.get_report()
							balance = trade.closing_balance
							trade_list.append(trade_report)
							break
							    
						if crossSL1:
							trade.set_closing_info_1(closing_time = time,
											 main_closing_price = moment_row[CLOSE],
											 aux_closing_price = moment_row[CLOSE],
											 closing_reason = 'stop loss')                                                
							# check takeprofit
						crossTP = ((trade.trade_type is SHORT and moment_row[CLOSE] < trade.Takeprofit) or
							   (trade.trade_type is LONG and moment_row[CLOSE] > trade.Takeprofit))

						if crossTP:
							trade.set_closing_info_1(closing_time = time,
											 main_closing_price = moment_row[CLOSE],
											 aux_closing_price = moment_row[CLOSE],
											 closing_reason = 'take profit')



			if (not in_trade) and not row['signal']:
				continue
			if (not in_trade) and row['signal'] == 1:
				if row['ATR'] != row['ATR']:
					continue
				in_trade = True
				trade = Trade(self.main_pair_name, self.aux_pair_name)
				trade.set_opening_info(opening_time = index,
						 main_open_price = df[OPEN][next_index],
						 aux_open_price = df[OPEN][next_index],
						 trade_type = LONG,
						 balance = balance,
						 ATR = row['ATR'],
						 risk = self.risk,
						 stop_loss1=  df[OPEN][next_index] - 1.5*row['ATR'],
						 stop_loss2 = df[OPEN][next_index] - 1.5*row['ATR'],
						 Pelleprice = df[OPEN][next_index] + row['ATR'],
						 Takeprofit = df[OPEN][next_index] + row['ATR'])


			if (not in_trade) and row['signal'] == -1:
				if row['ATR'] != row['ATR']:
					continue
				in_trade = True
				trade = Trade(self.main_pair_name, self.aux_pair_name)
				trade.set_opening_info(opening_time = index,
						 main_open_price = df[OPEN][next_index],
						 aux_open_price = df[OPEN][next_index],
						 trade_type = SHORT,
						 balance = balance,
						 ATR = row['ATR'],
						 risk = self.risk,
						 stop_loss1=  df[OPEN][next_index] + 1.5*row['ATR'],
						 stop_loss2 = df[OPEN][next_index] + 1.5*row['ATR'],
						 Pelleprice = df[OPEN][next_index] - row['ATR'],
						 Takeprofit = df[OPEN][next_index] - row['ATR'])



		trade_log = pd.DataFrame(trade_list)
		return trade_log
		



if __name__ == '__main__':
	GBPUSD_data = Pair(GBPUSD)
	# Dataframe for test
	dfall = GBPUSD_data.get_1D()
	df = dfall[-500:-200]# the five minutes time frame does not cover the 1 D range!!!!
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
