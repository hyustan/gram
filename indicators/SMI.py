import sys
import pandas as pd
sys.path.insert(0,'..')
from Indicator import Indicator
from utils.GlobalVariables import *


class SMI(Indicator):
        # Stochastic Momentum Index

        def __init__(self, period = 14, smoothing_period = 3):
                super(SMI, self).__init__()
                self.period = period
                self.smoothing_period = smoothing_period

        def calculate(self, df):
                '''
                returns the values of the stochastic momentum index
                :param: period: the period of the SMI indicator
                :param: smoothing_period: the smoothing period 
                :return: the SMI values as a panda series
                '''

                hig_max = df[HIGH].rolling(window = self.period).max()
                low_min = df[LOW].rolling(window = self.period).min()
                center = (hig_max + low_min) / 2 # center of low to high range
                dist2center = df[CLOSE] - center #subtract distance of Current Close from the Center of the Range.
                dist2center_smoothed = dist2center.ewm(span = self.smoothing_period).mean() # smooth distance to center with an exponential moving average
                dist2center_smoothed2 = dist2center_smoothed.ewm(span = self.smoothing_period).mean()
                range_price = hig_max - low_min
                range_smoothed = range_price.ewm(span = self.smoothing_period).mean() # smooth range with an exponential moving average
                range_smoothed2 = range_smoothed.ewm(span = self.smoothing_period).mean()
                out_series = dist2center_smoothed2/range_smoothed2

                return out_series
	
if __name__ == "__main__":
	df = pd.read_csv("..\data\Forex\GBPUSD\GBPUSD_1D.csv", index_col = 0)
	my_SMA = SMI(period = 14, smoothing_period = 3)
	print(my_SMA.calculate(df))
	



