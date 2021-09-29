from BPTK_Py import Model
from BPTK_Py import sd_functions as sd
from import_data import *
from general_functions import *


def set_model_logic(start_serial, stop_serial, df):
    """ Setup model based on start date, end date, and df containing input data """

    time_step_in_days = 2

    model = Model(
        starttime=start_serial,
        stoptime=stop_serial,
        dt=1.0 * time_step_in_days,
    )

    # create stocks (w/ initial values, and connect initial values)
    P_s, P_s_iv = create_model_stock(model, "Producer Stock")

    # create flows
    P_birth_f = model.flow("Birth Rate")
    P_death_f = model.flow("Total Death Rate")

    # create converters
    lifespan = model.converter("Average Lifespan")
    fertility = model.converter("Average Fertility")
    illness_death_rate = model.converter("Illness Death Rate")
    normal_death_rate = model.converter("Normal Death Rate")

    # create constants
    lifespan_bl = model.constant("Lifespan Baseline")
    fertility_bl = model.constant("Fertility Baseline")
    health = model.constant("Animal Health")
    illness_death_t = model.constant("Illness Death Time")

    # create data inputs (points AND corresponding converters)
    price_vam = create_model_data_variable(model, df, "Price (VAM)")
    cpi_fao = create_model_data_variable(model, df, "CPI (FAO)")

    # attach flows to stocks
    P_s.equation = P_birth_f - P_death_f

    # set equations for flows and converters
    lifespan.equation = lifespan_bl * health
    fertility.equation = fertility_bl
    P_birth_f.equation = P_s * fertility
    normal_death_rate.equation = P_s / lifespan
    illness_death_rate.equation = P_s * (1.0 - health) / illness_death_t
    P_death_f.equation = normal_death_rate + illness_death_rate

    # set default values for constants
    P_s_iv.equation = 100.0
    lifespan_bl.equation = 20.0 * 365.0
    fertility_bl.equation = 0.1 / 365.0
    health.equation = 1.0
    illness_death_t.equation = 0.5 * 365.0

    return model
