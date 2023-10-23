from pytrends.request import TrendReq
import matplotlib.pyplot as plt

pytrend = TrendReq()

#Compare word 'PSG and OM'
keywords = ["OM", "PSG"]

pytrend.build_payload(kw_list=keywords, timeframe='today 3-m')
data = pytrend.interest_over_time()

print(data)


data.plot()
plt.show()
