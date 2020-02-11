
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
    
		hig_max = df[High].rolling(window = self.period).max()
    low_min = df[LOW].rolling(window = self.period).min()
    center = (hig_max + low_min) / 2 # center of low to high range
		dist2center = df[CLOSE] –center #subtract distance of Current Close from the Center of the Range.
    dist2center_smoothed = dist2center.rolling(window = self.smoothing_period).ewm() # smooth distance to center with an exponential moving average
    dist2center_smoothed2 = dist2center_smoothed.rolling(window = self.smoothing_period).ewm()
    range = hig_max - low_min
    range_smoothed = range.rolling(window = self.smoothing_period).ewm() # smooth range with an exponential moving average
    range_smoothed2 = range_smoothed.rolling(window = self.smoothing_period).ewm()
    out_series = dist2center_smoothed2/range_smoothed2
    
		return out_series




