# Adding parent directory to the PYTHONPATH
import sys
import gc
sys.path.insert(0,'..')
import numpy as np
import pandas as pd
from utils.GlobalVariables import *
import BaseTrader

class RowTrader():

        # The trade's method of this class will iterate over rows
        # it predicts one row at a time

        def __init__(self,df,df_moment):
                self.df = df
                self.df_moment = df_moment
                
        def simulate(self):
                # Report should be dataframe of all trades consisiting the trades' reports
                # Trades' report is a dictionary. You may find it in the Trade class in the same folder
                # total_profit is the sum of all trades' profits

                # Iterate over rows
                in_trade = False
                trade_list = []
                for index,next_index in izip(df.index[:-1],df.index[1:]):
                        row = df.loc[index]
                        # check opposit signal
                        if in_trade:
                                negativeSignal = ((trade['trade_type'] is 'SHORT' and row['signal'] is 1) or
                                                  (trade['trade_type'] is 'LONG' and row['signal'] is -1))
                                if negativeSignal:
                                        in_trade = False
                                        if 'close_trade1' not in trade:
                                                trade.update({'close_trade1' : row[CLOSE],'closeReason' : 'opposit signal'})
                                                trade.update({'close_trade2' : row[CLOSE],'closeReason' : 'opposit signal'})
                                                trade_list.append(trade)
                                        # check pelle                        
                                        if trade['trade_type'] is 'LONG' and row[CLOSE] > trade['Pelleprice']:
                                                trade['Stoploss_trade2'] = trade['Pelleprice']-ATR
                                                trade['Pelleprice'] = trade['Pelleprice']+ATR
                                        if trade_type is 'SHORT' and row[CLOSE] < trade['Pelleprice']:
                                                trade['Stoploss'] = trade['Pelleprice']+ATR
                                                trade['Pelleprice'] = trade['Pelleprice']-ATR
                                else:
                                        for moment_row in df_moment[index:nex_index]:
                                                # check stoploss
                                                crossSL1 = ((trade['trade_type'] is 'SHORT' and moment_row[CLOSE] > trade['Stoploss_trade1']) or
                                                            (trade['trade_type'] is 'LONG' and moment_row[CLOSE] < trade['Stoploss_trade1']))

                                                crossSL2 = ((trade['trade_type'] is 'SHORT' and moment_row[CLOSE] > trade['Stoploss_trade2']) or
                                                            (trade['trade_type'] is 'LONG' and moment_row[CLOSE] < trade['Stoploss_trade2']))

                                                if crossSL2:
                                                        in_trade = False
                                                if 'close_trade1' not in trade:
                                                        trade.update({'close_trade1' : moment_row[CLOSE],'closeReason' : 'stop loss'})
                                                        trade.update({'close_trade2' : row[CLOSE],'closeReason' : 'stop loss'})
                                                        trade_list.append(trade)
                                                        break
                                                if crossSL1:
                                                        trade.update({'close_trade1' : row[CLOSE],'closeReason1' : 'stop loss'})                                                  
                                                        # check takeprofit
                                                        crossTP = ((trade['trade_type'] is 'SHORT' and moment_row[CLOSE] < trade['Takeprofit']) or
                                                        (trade['trade_type'] is 'LONG' and moment_row[CLOSE] > trade['Takeprofit']))

                                                if crossTP:
                                                        trade.update({'close_trade1' : row[CLOSE],'closeReason' : 'take profit'})



                        if not in_trade and not row['signal']:
                                continue
                        if not in_trade and row['signal'] is 1:
                                in_trade = True
                                trade={'trade_type' : 'LONG',
                                       'open' : df[OPEN][next_index].value+spread,
                                       'Stoploss_trade1':  df[OPEN][next_index].value - 1.5*ATR,
                                       'Stoploss_trade2' : df[OPEN][next_index].value - 1.5*ATR,
                                       'Pelleprice' : df[OPEN][next_index].value + ATR,
                                       'Takeprofit' : df[OPEN][next_index].value + ATR}

                        if (not in_trade) and row['signal'] is -1:
                                in_trade = True
                                trade = {'trade_type' : 'SHORT',
                                         'open' : df[OPEN][next_index].value - spread,
                                         'Stoploss_trade1' : df[OPEN][next_index].value + 1.5*ATR,
                                         'Stoploss_trade2' : df[OPEN][next_index].value + 1.5*ATR,
                                         'Pelleprice' : df[OPEN][next_index].value - ATR,
                                         'Takeprofit' : df[OPEN][next_index].value - ATR}


                trade_log = pd.DataFrame(trade_list)            
                return trade_log
if __name__ == '__main__':
        GBPUSD_data = Pair(GBPUSD)
        # Dataframe for test
        df = GBPUSD_data.get_1D()
        df_moment = GBPUSD_data
        row_trader = RowTrader(df,df_moment)
        trade_log = row_trader.simulate()
