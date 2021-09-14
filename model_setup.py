from BPTK_Py import Model
from BPTK_Py import sd_functions as sd
import numpy as np
import pandas as pd


def new_stock():
    global var_id
    var = model.stock(str(var_id))
    var_id += 1
    var_iv = model.constant(str(var_id))
    var_id += 1
    var.initial_value = var_iv
    return var, var_iv


def new_flow():
    global var_id
    var = model.flow(str(var_id))
    var_id += 1
    return var


def new_converter():
    global var_id
    var = model.converter(str(var_id))
    var_id += 1
    return var


def new_constant():
    global var_id
    var = model.constant(str(var_id))
    var_id += 1
    return var


num_years = 10
time_step_in_days = 0.5

model = Model(
    starttime=0.0,
    stoptime=365 * num_years,
    dt=1.0 * time_step_in_days,
    name='ETH_livestock'
)

var_id = 0

# create stocks (w/ initial values)
producer_stock, producer_stock_iv = new_stock()

# create flows
birth_rate = new_flow()
death_rate = new_flow()
illness_death_rate = new_flow()

# create converters
lifespan = new_converter()
fertility = new_converter()

# create constants
lifespan_baseline = new_constant()
fertility_baseline = new_constant()
animal_health = new_constant()
illness_death_time = new_constant()
producer_stock_initial_value = new_constant()

# attach flows to stocks
producer_stock.equation = birth_rate - death_rate - illness_death_rate

# set equations for flows and converters
lifespan.equation = lifespan_baseline * animal_health
fertility.equation = fertility_baseline #* animal_health
birth_rate.equation = producer_stock * fertility
death_rate.equation = producer_stock / lifespan
illness_death_rate.equation = producer_stock * (1-animal_health) / illness_death_time

# set default values for constants
producer_stock_iv.equation = 100.0
lifespan_baseline.equation = 20.0 * 365
fertility_baseline.equation = 0.1 / 365
animal_health.equation = 1.0
illness_death_time.equation = 0.5 * 365
