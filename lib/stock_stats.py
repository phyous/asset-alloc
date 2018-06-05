import math
import numpy as np
from datetime import datetime

# Calculate standard deviation of return & mean
# 1, 3, 5, 10, 20 year
# https://www.investopedia.com/walkthrough/corporate-finance/4/return-risk/expected-return.aspx
class StockStats:
	YEAR_RANGES = [1, 3, 5, 10, 20]

	def __init__(self, vals):
		self.vals = vals
		self.annual_close = self.compute_annual_close(vals)
		self.annual_return_rates = self.compute_annual_return_rates()
		self.annualized_return_rates = self.compute_annualized_return_rates()
		self.std = self.compute_stdevs()

	def earlierst_value(self):
		return self.vals[0][0]

	# get the closing price for every year
	def compute_annual_close(self, v):
		prices = {}
		for l in v:
			date = datetime.strptime(l[0], '%Y-%M-%d')
			close = float(l[1])
			if date.year in prices:
				cur = prices[date.year]
				prices[date.year] = cur if (date < cur[1]) else (close, date)
			else:
				prices[date.year] = (close, date)
		return [(k, v[0]) for k, v in prices.items()]

	# compute average return for every year
	def compute_annual_return_rates(self):
		return [(self.annual_close[val][0], (self.annual_close[val][1] - self.annual_close[val-1][1])  / self.annual_close[val-1][1]) for val in range(1, len(self.annual_close))]

	# compute the annualized rates for the last n in an array
	def annualized_rates(self, vs, n):
		pows = [math.pow(1+v[1], 1/n) for v in vs[-n:]]
		product = 1
		for p in pows:
			product *= p
		return product - 1

	def compute_annualized_return_rates(self):
		ar = {}
		for r in filter(lambda x: x <= len(self.annual_return_rates), self.YEAR_RANGES):
			ar[r] = self.annualized_rates(self.annual_return_rates, r)
		return ar

		# Mean returns by YEAR_RANGES intervals
	def compute_means(self):
		means = {}
		for r in filter(lambda x: x <= len(self.annual_return_rates), self.YEAR_RANGES):
			means[r] = sum([i[1] for i in self.annual_return_rates[-r:]])/r
		return means

	# variance of returns by YEAR_RANGES intervals
	def compute_stdevs(self):
		std = {}
		for r in filter(lambda x: x <= len(self.annual_return_rates), self.YEAR_RANGES):
			std[r] = np.std([i[1] for i in self.annual_return_rates[-r:]])
		return std