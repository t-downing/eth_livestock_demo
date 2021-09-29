import BPTK_Py
from model_config import set_model_logic
from datetime import datetime
from general_functions import *


def setup_model(start_date, end_date, df):
    start_serial, end_serial = datetime_to_serial([start_date, end_date])
    model = set_model_logic(start_serial, end_serial, df)
    model_env = BPTK_Py.bptk()
    model_env.register_model(model)
    scenario_manager = {
        "scenario_manager": {
            "model": model
        }
    }
    model_env.register_scenario_manager(scenario_manager)
    return model_env, model


def run_model(model_env, model, scenario_name, constants, start_date, stop_date):
    """ Run model with constants and dates, output df of results """

    # set dates
    model.starttime = datetime_to_serial(start_date)
    model.stoptime = datetime_to_serial(stop_date)

    # register scenario
    model_env.register_scenarios(
        scenarios={
            scenario_name: {
                "constants": constants
            },
        },
        scenario_manager="scenario_manager"
    )

    variables = [str(var) for var in model.stocks] \
                + [str(var) for var in model.flows] \
                + [str(var) for var in model.converters] \
                + [str(var) for var in model.constants]
    df = model_env.plot_scenarios(
        scenarios=scenario_name,
        scenario_managers="scenario_manager",
        equations=variables,
        return_df=True
    ).reset_index()
    df["Scenario"] = scenario_name
    df["Date"] = serial_to_datetime(df["t"])
    df["t_check"] = datetime_to_serial(df["Date"])
    return df




