import pandas as pd
import BPTK_Py
import plotly.express as px
import time
from model_operations import *
from datetime import datetime
from import_data import *

# read data into df
df_input = import_all_data()

# setup model
start_date, stop_date = datetime(2020, 1, 1), datetime.now()
model_env, model = setup_model(start_date, stop_date, df_input)

print(f"start is {model.starttime}, stop is {model.stoptime}")

# run base scenario
df = run_model(model_env, model, "base", {}, start_date, stop_date)

px.line(df, x="Date", y=["CPI (FAO)"]).show()


