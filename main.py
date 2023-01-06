#!/usr/bin/env python3

import datetime
from os import environ, makedirs
from os.path import isfile, isdir
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from get_prices import *
from manage_products import FILE as LIST_FILE


# Portuguese date format
DATE = datetime.date.today().strftime("%d/%m/%Y")

FILE = "products_price.tab"
PLOTS_DIR = "plots/"


def suppress_warnings():
    """Suppress warnings of matplotlib.
    """

    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


def create_file():
    """Creates the FILE in case it doesn't exist.
    """

    if not (isfile(FILE)):
        with open(FILE, "w") as f:
            f.write("DATE\tLINK\tPRODUCT\tPRICE\n")


def delete_today_data():
    """Function to delete all the lines of FILE that starts with DATE.
    """

    with open(FILE) as f:
        lines = f.readlines()

    with open(FILE, "w") as f:
        for line in lines:
            check_date = line.split("\t")[0]
            if check_date == DATE:
                continue

            f.write(line)            


def get_data():
    """Get data from LIST_FILE

    Returns:
        tuple: 2D tuple with the links and the name of the products in the order of LIST_FILE.
    """

    df = pd.read_table(LIST_FILE)
    links = list(df["LINK"])
    products = list(df["PRODUCT"])
    return links, products


def get_price(link):
    """Get the price of the item of the link.

    Args:
        link (str): link of the page with the item

    Returns:
        float: price of the item of the link
    """

    headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0' }
    r = requests.get(link, headers=headers).text
    soup = bs(r, "html.parser")

    if "www.nike.com/" in link:
        price = get_price_nike(soup)
    elif "www.adidas." in link:
        price = get_price_adidas(soup)
    else:
        price = None
        link = link.replace("https://", "")
        link = link.split("/")[0]
        print(f"Program not implemented for {link}")
    
    price = float(price.replace(",", "."))

    return price


def create_plot(df):
    """Plot the figure with the price evolution of an item.

    Args:
        df (pandas.core.frame.DataFrame): dataframe with the prices of an specific item
    """

    date = DATE.replace("/", "_")
    dir = PLOTS_DIR + date + "/"

    if not isdir(dir):
        makedirs(dir)

    x = df["DATE"]
    y = df["PRICE"]
    product = list(df["PRODUCT"])[0]

    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.title(product)
    plt.xlabel("Date (dd/mm/yyyy)")
    plt.ylabel("Price (€)")
    plt.savefig(dir + product.replace(" ", "_") + ".png", bbox_inches='tight')


def main():

    suppress_warnings()
    create_file()

    with open(FILE, "r") as f:
        lines = f.readlines()
    
    date_last_day = lines[-1].split("\t")[0]
    
    if date_last_day == DATE:
        print("Script already executed today.")
        response = input(
            "Do you want to force it execute it again "
            + "(data may be overwritten)? [Y/N] "
            )
        response = "Y"
        if response in ("y", "Y"):
            print("Today's data will be overwritten")
            delete_today_data()
        else:
            exit()
    
    links, products = get_data()

    with open(FILE, "a") as f:
        for link, product in zip(links, products):
            price = get_price(link)
            f.write(f"{DATE}\t{link}\t{product}\t{price}\n")
        
    
    df = pd.read_table(FILE)

    for product in products:
        product_df = df[df["PRODUCT"] == product]
        create_plot(product_df)


if __name__ == '__main__':
    main()
