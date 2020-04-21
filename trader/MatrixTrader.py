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

class MatrixTrader():

        # The trade's method of this class will iterate over rows
        # it predicts one row at a time

        def __init__(self,main_pair_name, aux_pair_name,df,df_moment,balance):
                self.main_pair_name = main_pair_name
                self.aux_pair_name = aux_pair_name
                self.df = df
                self.df_moment = df_moment
                self.balance = balance
                
        def simulate(self):
                # Report should be dataframe of all trades consisiting the trades' reports
                # Trades' report is a dictionary. You may find it in the Trade class in the same folder
                # total_profit is the sum of all trades' profits

                # Iterate over rows
                in_trade = False
                trade_list = []
                balance = self.balance
                for index,next_index in zip(df.index[:-1],df.index[1:]):
                        print('bing')
                        row = df.loc[index]
                        # check opposit signal
                        if in_trade:
                                negativeSignal = ((trade.trade_type is 'SHORT' and row['signal'] is 1) or
                                                  (trade.trade_type is 'LONG' and row['signal'] is -1))
                                if negativeSignal:
                                        in_trade = False
                                        if main_closing_price_1 not in trade:
                                                trade.set_closing_info_1(closing_time = index, main_closing_price = row[CLOSE],
                                                                         aux_closing_price = row[CLOSE], closing_reason = 'opposit signal')
                                        trade.set_closing_info_2(closing_time = index, main_closing_price = row[CLOSE],
                                                                 aux_closing_price = row[CLOSE], closing_reason = 'opposit signal')

                                        trade.evaluate()
                                        trade_report = trade.get_report()
                                        balance = trade.closing_balance()
                                        trade_list.append(trade_report)
                                        # check pelle                        
                                        if trade.trade_type is 'LONG' and row[CLOSE] > trade.Pelleprice:
                                                trade.Stoploss_trade2 = trade.Pelleprice-ATR
                                                trade.Pelleprice = trade.Pelleprice+ATR
                                        if trade.trade_type is 'SHORT' and row[CLOSE] < trade.Pelleprice:
                                                trade.stop_loss2 = trade.Pelleprice+ATR
                                                trade.Pelleprice = trade.Pelleprice-ATR
                                else:
                                        for moment_row in df_moment[index:nex_index]:
                                                # check stoploss
                                                crossSL1 = ((trade.trade_type is 'SHORT' and moment_row[CLOSE] > trade.Stoploss_trade1) or
                                                            (trade.trade_type is 'LONG' and moment_row[CLOSE] < trade.Stoploss_trade1))

                                                crossSL2 = ((trade.trade_type is 'SHORT' and moment_row[CLOSE] > trade.Stoploss_trade2) or
                                                            (trade.trade_type is 'LONG' and moment_row[CLOSE] < trade.Stoploss_trade2))

                                                if crossSL2:
                                                        in_trade = False
                                                        if 'close_trade1' not in trade:
                                                                trade.set_closing_info_1(closing_time = moment_row.index,
                                                                                         main_closing_price = moment_row[CLOSE],
                                                                                         aux_closing_price = moment_row[CLOSE],
                                                                                         closing_reason = 'stop loss')

                                                        trade.set_closing_info_2(closing_time = moment_row.index,
                                                                                         main_closing_price = moment_row[CLOSE],
                                                                                         aux_closing_price = moment_row[CLOSE],
                                                                                         closing_reason = 'stop loss')
                                                        trade.evaluate()
                                                        trade_report = trade.get_report()
                                                        balance = trade.closing_balance()
                                                        trade_list.append(trade_report)
                                                        break
                                                            
                                                if crossSL1:
                                                        trade.update(closing_time = moment_row.index,
                                                                                         main_closing_price = moment_row[CLOSE],
                                                                                         aux_closing_price = moment_row[CLOSE],
                                                                                         closing_reason = 'stop loss')                                                
                                                        # check takeprofit
                                                crossTP = ((trade.trade_type is 'SHORT' and moment_row[CLOSE] < trade.Takeprofit) or
                                                           (trade.trade_type is 'LONG' and moment_row[CLOSE] > trade.Takeprofit))

                                                if crossTP:
                                                        trade.set_closing_info_1(closing_time = moment_row.index,
                                                                                         main_closing_price = moment_row[CLOSE],
                                                                                         aux_closing_price = moment_row[CLOSE],
                                                                                         closing_reason = 'take profit')



                        if (not in_trade) and not row['signal']:
                                continue
                        if (not in_trade) and row['signal'] == 1:
                                in_trade = True
                                main_pair_name = self.main_pair_name
                                aux_pair_name = self.aux_pair_name
                                trade = Trade(main_pair_name, aux_pair_name)
                                trade.set_opening_info(opening_time = row.index,
                                                 main_open_price = df[OPEN][next_index],
                                                 aux_open_price = df[OPEN][next_index],
                                                 trade_type = 'LONG',
                                                 balance = balance,
                                                 ATR = ATR,
                                                 risk = risk,
                                                 stop_loss1=  df[OPEN][next_index] - 1.5*ATR,
                                                 stop_loss2 = df[OPEN][next_index] - 1.5*ATR,
                                                 Pelleprice = df[OPEN][next_index] + ATR,
                                                 Takeprofit = df[OPEN][next_index] + ATR)


                        if (not in_trade) and row['signal'] == -1:
                                in_trade = True
                                trade = Trade(main_pair_name, aux_pair_name)
                                trade.set_opening_info(opening_time = row.index,
                                                 main_open_price = df[OPEN][next_index].value,
                                                 aux_open_price = df[OPEN][next_index].value,
                                                 trade_type = 'SHORT',
                                                 balance = balance,
                                                 ATR = ATR,
                                                 risk = risk,
                                                 stop_loss1=  df[OPEN][next_index].value + 1.5*ATR,
                                                 stop_loss2 = df[OPEN][next_index].value + 1.5*ATR,
                                                 Pelleprice = df[OPEN][next_index].value - ATR,
                                                 Takeprofit = df[OPEN][next_index].value - ATR)



                trade_log = pd.DataFrame(trade_list)            
                return trade_log
if __name__ == '__main__':
        GBPUSD_data = Pair(GBPUSD)
        # Dataframe for test
        df = GBPUSD_data.get_1D()
        df['signal'] = 1
        df_moment = GBPUSD_data.get_5M()
        matrix_trader = MatrixTrader('GBPUSD','GBPUSD',df,df_moment,1000)
        trade_log = matrix_trader.simulate()
