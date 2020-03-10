# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *
from feature_generator.FG import FG

import pandas as pd

# Importing some indicators for generating features
from indicators.EMA import EMA
from indicators.AroonHorn import AroonHorn
from indicators.SuperTrend import SuperTrend
from indicators.SqueezeBreak import SqueezeBreak

from indicators_transformer.EMA_FT import EMA_FT
from indicators_transformer.AroonHorn_FT import AroonHorn_FT
from indicators_transformer.SuperTrend_FT import SuperTrend_FT
from indicators_transformer.SqueezeBreak_FT import SqueezeBreak_FT


class FG1(FG):
	# Base class for all of the feature transformers
	def __init__(self):
		super(FG1, self).__init__()

	def generate_all_features(self, df):

		# Calculating indicators
		baseline = EMA(20, CLOSE).calculate(df)
		first_trend_ind = SuperTrend(10, 3).calculate(df)
		second_trend_ind = AroonHorn(20).calculate(df)
		volume = SqueezeBreak(20, 20).calculate(df)

		baseline = EMA_FT().transform(df, baseline)
		first_trend_ind = SuperTrend_FT().transform(df, first_trend_ind)
		second_trend_ind = AroonHorn_FT().transform(df, second_trend_ind)
		volume = SqueezeBreak_FT().transform(df, volume)

		features = pd.concat([baseline, first_trend_ind, second_trend_ind, volume], join = 'inner', axis = 1)

		print (features)

	

if __name__ == "__main__":
	# Loading the data
	from data.FXDataLoader import Pair
	GBPUSD_data = Pair(GBPUSD)

	# Dataframe for test
	df = GBPUSD_data.get_1D()

	fg = FG1()
	fg.generate_all_features(df)


