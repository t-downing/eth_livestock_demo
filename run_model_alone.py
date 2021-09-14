from model_setup import *
import pandas as pd
import matplotlib.pyplot as plt

#df1 = pd.DataFrame(columns=["time", "values"])

df1 = producer_stock.plot(return_df=True).reset_index()
df2 = death_rate.plot(return_df=True).reset_index()


print(df1.iloc[:,1])

print(df2.iloc[:,1])

plt.interactive(False)
#plt.show()

