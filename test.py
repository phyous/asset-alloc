import pandas_datareader.data as web
from datetime import datetime

start = datetime(1988, 1, 1)
end = datetime(2018, 5, 13)

f = web.DataReader('F', 'morningstar', start, end)