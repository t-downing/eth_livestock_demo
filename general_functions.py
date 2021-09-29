from datetime import datetime
from BPTK_Py import sd_functions as sd
from BPTK_Py import Model
import pandas as pd


def datetime_to_serial(dates):
    """ Convert datetime into Excel serial number """
    serials = []
    try:
        for date in dates:
            timestamp = datetime.timestamp(date)
            serials.append(timestamp / 86400.0 + 25568.0)
    except TypeError:
        date = dates
        timestamp = datetime.timestamp(date)
        serials = timestamp / 86400.0 + 25568.0
    return serials


def serial_to_datetime(serials):
    """ Convert Excel serial number into datetime """
    dates = []
    try:
        for serial in serials:
            seconds = (serial - 25568.0) * 86400.0
            dates.append(datetime.utcfromtimestamp(seconds))
    except TypeError:
        serial = serials
        seconds = (serial - 25568.0) * 86400.0
        dates = datetime.utcfromtimestamp(seconds)
    return dates


def df_to_lookup(df, var_name):
    """ Create list for model lookup from central external data df """
    df = df[[var_name]].dropna().reset_index()
    df["Date"] = datetime_to_serial(df["Date"])
    list_out = df.values.tolist()
    return list_out


def create_model_stock(model, stock_name):
    """ Create stock and stock initial value """
    stock_var = model.stock(stock_name)
    stock_initial_value_var = model.constant(f"{stock_name} Initial Value")
    stock_var.initial_value = stock_initial_value_var
    return stock_var, stock_initial_value_var


def create_model_data_variable(model, df, data_name):
    """ Create a variable that reads external data from the central df """
    data_var = model.converter(data_name)
    model.points[data_name] = df_to_lookup(df, data_name)
    data_var.equation = sd.lookup(sd.time(), data_name)
    return data_var