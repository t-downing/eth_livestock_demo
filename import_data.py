import hdx.hdx_configuration
import pandas as pd
import plotly.express as px

from hdx.utilities.easy_logging import setup_logging
from hdx.hdx_configuration import Configuration
from hdx.data.dataset import Dataset


def import_all_data():
    """ Read all data from CSV files and store in one df """
    df = pd.DataFrame()
    market  = "Gode"
    commodity = "Livestock (Goat)"
    output_col = "Price (VAM)"
    df = pd.concat([df, read_vam(commodity, market, output_col)], axis=1)
    output_col = "CPI (FAO)"
    df = pd.concat([df, read_fao_inflation(output_col)], axis=1)
    return df.sort_index()


def download_all_data():
    """ Download all recent datasets and save them as CSVs """
    download_from_hdx("wfp-food-prices-for-ethiopia")
    download_from_hdx("faostat-prices-for-ethiopia")
    return


def download_from_hdx(hdx_name, resource_number=0):
    """ Download most recent dataset from HDX and save as CSV """
    setup_logging()
    try:
        Configuration.create(hdx_site='prod', user_agent='SD_model_demo', hdx_read_only=True)
    except hdx.hdx_configuration.ConfigurationError:
        pass
    dataset = Dataset.read_from_hdx(hdx_name)
    resources = dataset.get_resources()
    url = resources[resource_number]["download_url"]
    filename = url[url.rfind("/")+1:]
    df = pd.read_csv(url)
    path = f"data/{filename}"
    df.to_csv(path)
    return


def read_vam(commodities, market, output_col):
    """ Read VAM data from CSV and output df """
    filename = "data/wfp_food_prices_eth.csv"
    df = pd.read_csv(filename, skiprows=[1])
    df["Date"] = pd.to_datetime(df["date"])

    # pick commodity
    # all_commodities = df["commodity"].unique()
    # print(all_commodities)
    try:
        df = df[df["commodity"].isin(commodities)]
    except TypeError:
        df = df[df["commodity"] == commodities]

    # pick market
    df = df[df["market"] == market]

    # correct units
    def price_to_kg_price(unit, price):
        index = unit.find("KG")
        if index == 0 or index == -1:
            kgs = 1.0
        else:
            kgs = float(unit[:index-1])
        return price / kgs
    df["unit-price"] = df["price"].copy()
    df["price"] = df.apply(lambda x: price_to_kg_price(x["unit"], x["price"]), axis=1)

    df.rename(columns={"price": output_col}, inplace=True)
    df = df[["Date", output_col]].set_index("Date")
    return df


def read_fao_inflation(output_col):
    # read file and set date
    filename = "data/consumer-price-indices_eth.csv"
    df = pd.read_csv(filename, skiprows=[1])
    df["Date"] = pd.to_datetime(df["StartDate"])
    # filter df
    df = df[df["Item"] == "Consumer Prices, General Indices (2015 = 100)"]
    # correct naming
    df.rename(columns={"Value": output_col}, inplace=True)
    # select single column
    df = df[["Date", output_col]].set_index("Date")
    return df

