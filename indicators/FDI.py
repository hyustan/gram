# Adding parent directory to the PYTHONPATH
import sys
import pandas as pd
import numpy as np
sys.path.insert(0,'..')
from Indicator import Indicator
from utils.GlobalVariables import *

class FDI(Indicator):
    # Fractal dimension index
    # the code is based on my understanding from the code in the test folder
    # and the webpage https://www.prorealcode.com/prorealtime-indicators/fractal-dimension-index-fdi/
    # I have put a picture from the formulation in test folder too

    def __init__(self, period = 14):
        super(FDI, self).__init__()
        self.period = period

    def calculate(self,df):
        '''
        returns the values of fractal dimension in a numpy array
        :param: period: the period of Fractal dimension
        '''
        hig_max = df[HIGH].rolling(window = self.period).max()
        low_min = df[LOW].rolling(window = self.period).min()
        range_price = hig_max - low_min
        FDI = np.zeros(len(range_price))
        for i in range(self.period,len(df[CLOSE])):
            normalized_price = (df[CLOSE][i-self.period:i] - low_min[i])/range_price[i]
            diff = np.diff(normalized_price)
            length = np.sqrt(diff**2+1/self.period**2)
            sum_length = np.sum(length)
            FDI[i] = 1+np.log(sum_length*2)/np.log(2*self.period)
        return FDI

if __name__ == "__main__":
    df = pd.read_csv("..\data\Forex\GBPUSD\GBPUSD_1D.csv", index_col = 0)
    my_FDI = FDI(period = 20)
    df['FDI(20)'] = my_FDI.calculate(df)
    df.to_csv("FDI_test.csv")
