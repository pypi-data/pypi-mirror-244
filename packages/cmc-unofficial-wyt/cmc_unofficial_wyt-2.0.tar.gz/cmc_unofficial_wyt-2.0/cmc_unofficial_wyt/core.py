#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Rohit Gupta'

from __future__ import print_function

__all__ = ["CmcScraper"]

import os
import csv
import sys
import tablib
import warnings
from datetime import datetime
from datetime import date
from datetime import timezone
from datetime import timedelta
from requests import get

def get_url_data(url, proxies):
    """
    This method downloads the data of the web page.
    :param url: 'url' of the web page to download
    :return: response object of get request of the 'url'
    """

    try:
        response = get(url, proxies=proxies)
        return response
    except Exception as e:
        if hasattr(e, "message"):
            print("Error message (get_url_data) :", e.message)
        else:
            print("Error message (get_url_data) :", e)
        raise e


def get_coin_id(coin_code, proxies):
    """
    This method fetches the name(id) of currency from the given code
    :param coin_code: coin code of a cryptocurrency e.g. btc
    :return: coin-id for the a cryptocurrency on the coinmarketcap.com
    """

    api_url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/map?symbol={coin_code}".format(coin_code=coin_code)

    try:
        json_data = get_url_data(api_url, proxies).json()
        error_code = json_data["status"]["error_code"]
        if error_code == 0:
            return json_data["data"][0]["slug"]
        if error_code == 400:
            raise InvalidCoinCode(
                "'{}' coin code is unavailable on coinmarketcap.com".format(coin_code)
            )
        else:
            raise Exception(json_data["status"]["error_message"])
    except Exception as e:
        print("Error fetching coin id data for coin code {}", coin_code)
        if hasattr(e, "message"):
            print("Error message:", e.message)
        else:
            print("Error message:", e)


def download_coin_data(coin_code, start_date, end_date, fiat, proxies):
    """
    Download HTML price history for the specified cryptocurrency and time range from CoinMarketCap.

    :param coin_code: coin code of a cryptocurrency e.g. btc
    :param start_date: date since when to scrape data (in the format of dd-mm-yyyy)
    :param end_date: date to which scrape the data (in the format of dd-mm-yyyy)
    :param fiat: fiat code eg. USD, EUR
    :return: returns html of the webpage having historical data of cryptocurrency for certain duration
    """

    if start_date is None:
        # default start date on coinmarketcap.com
        start_date = "28-4-2013"
    if end_date is None:
        yesterday = date.today() - timedelta(1)
        end_date = yesterday.strftime("%d-%m-%Y")

    coin_id = get_coin_id(coin_code, proxies)

    # convert the dates to timestamp for the url
    start_date_timestamp = int(
        (
                datetime.strptime(start_date, "%d-%m-%Y")
                - timedelta(days=1)
        )
        .replace(tzinfo=timezone.utc)
        .timestamp()
    )

    end_date_timestamp = int(
        datetime.strptime(end_date, "%d-%m-%Y")
        .replace(tzinfo=timezone.utc)
        .timestamp()
    )

    api_url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?convert={}&slug={}&time_end={}&time_start={}".format(
        fiat, coin_id, end_date_timestamp, start_date_timestamp
    )

    try:
        json_data = get_url_data(api_url, proxies).json()
        if json_data["status"]["error_code"] != 0:
            raise Exception(json_data["status"]["error_message"])
        return json_data
    except Exception as e:
        print(
            "Error fetching price data for {} for interval '{}' and '{}'",
            coin_code,
            start_date,
            end_date,
        )
        if hasattr(e, "message"):
            print("Error message (download_data) :", e.message)
        else:
            print("Error message (download_data) :", e)
        return {}


def _replace(s, bad_chars):
    if sys.version_info > (3, 0):
        # For Python 3
        without_bad_chars = str.maketrans("", "", bad_chars)
        return s.translate(without_bad_chars)
    else:
        # For Python 2
        import string

        identity = string.maketrans("", "")
        return s.translate(identity, bad_chars)


class InvalidParameters(ValueError):
    """Passed parameters are invalid."""


class InvalidCoinCode(NotImplementedError):
    """This coin code is unavailable on 'coinmarketcap.com'"""


def get_url_data(url, proxies):
    """
    This method downloads the data of the web page.
    :param url: 'url' of the web page to download
    :return: response object of get request of the 'url'
    """

    try:
        response = get(url, proxies=proxies)
        return response
    except Exception as e:
        if hasattr(e, "message"):
            print("Error message (get_url_data) :", e.message)
        else:
            print("Error message (get_url_data) :", e)
        raise e


def get_coin_id(coin_code, proxies):
    """
    This method fetches the name(id) of currency from the given code
    :param coin_code: coin code of a cryptocurrency e.g. btc
    :return: coin-id for the a cryptocurrency on the coinmarketcap.com
    """

    api_url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/map?symbol={coin_code}".format(coin_code=coin_code)

    try:
        json_data = get_url_data(api_url, proxies).json()
        error_code = json_data["status"]["error_code"]
        if error_code == 0:
            return json_data["data"][0]["slug"]
        if error_code == 400:
            raise InvalidCoinCode(
                "'{}' coin code is unavailable on coinmarketcap.com".format(coin_code)
            )
        else:
            raise Exception(json_data["status"]["error_message"])
    except Exception as e:
        print("Error fetching coin id data for coin code {}", coin_code)
        if hasattr(e, "message"):
            print("Error message:", e.message)
        else:
            print("Error message:", e)


def download_coin_data(coin_code, start_date, end_date, fiat, proxies):
    """
    Download HTML price history for the specified cryptocurrency and time range from CoinMarketCap.

    :param coin_code: coin code of a cryptocurrency e.g. btc
    :param start_date: date since when to scrape data (in the format of dd-mm-yyyy)
    :param end_date: date to which scrape the data (in the format of dd-mm-yyyy)
    :param fiat: fiat code eg. USD, EUR
    :return: returns html of the webpage having historical data of cryptocurrency for certain duration
    """

    if start_date is None:
        # default start date on coinmarketcap.com
        start_date = "28-4-2013"
    if end_date is None:
        yesterday = date.today() - timedelta(1)
        end_date = yesterday.strftime("%d-%m-%Y")

    coin_id = get_coin_id(coin_code, proxies)

    # convert the dates to timestamp for the url
    start_date_timestamp = int(
        (
                datetime.strptime(start_date, "%d-%m-%Y")
                - timedelta(days=1)
        )
        .replace(tzinfo=timezone.utc)
        .timestamp()
    )

    end_date_timestamp = int(
        datetime.strptime(end_date, "%d-%m-%Y")
        .replace(tzinfo=timezone.utc)
        .timestamp()
    )

    api_url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?convert={}&slug={}&time_end={}&time_start={}".format(
        fiat, coin_id, end_date_timestamp, start_date_timestamp
    )

    try:
        json_data = get_url_data(api_url, proxies).json()
        if json_data["status"]["error_code"] != 0:
            raise Exception(json_data["status"]["error_message"])
        return json_data
    except Exception as e:
        print(
            "Error fetching price data for {} for interval '{}' and '{}'",
            coin_code,
            start_date,
            end_date,
        )
        if hasattr(e, "message"):
            print("Error message (download_data) :", e.message)
        else:
            print("Error message (download_data) :", e)
        return {}


def _replace(s, bad_chars):
    if sys.version_info > (3, 0):
        # For Python 3
        without_bad_chars = str.maketrans("", "", bad_chars)
        return s.translate(without_bad_chars)
    else:
        # For Python 2
        import string

        identity = string.maketrans("", "")
        return s.translate(identity, bad_chars)


class InvalidParameters(ValueError):
    """Passed parameters are invalid."""


class InvalidCoinCode(NotImplementedError):
    """This coin code is unavailable on 'coinmarketcap.com'"""


class CmcScraper(object):
    """
    Scrape cryptocurrency historical market price data from coinmarketcap.com

    """

    def __init__(self,
                 coin_code,
                 start_date=None,
                 end_date=None,
                 all_time=False,
                 order_ascending=False,
                 fiat="USD",
                 proxies=None):
        """
        :param coin_code: coin code of cryptocurrency e.g. btc
        :param start_date: date since when to scrape data (in the format of dd-mm-yyyy)
        :param end_date: date to which scrape the data (in the format of dd-mm-yyyy)
        :param all_time: 'True' if need data of all time for respective cryptocurrency
        :param order_ascending: data ordered by 'Date' in ascending order (i.e. oldest first).
        :param fiat: fiat code eg. USD, EUR
        """

        self.coin_code = coin_code
        self.start_date = start_date
        self.end_date = end_date
        self.all_time = bool(all_time)
        self.order_ascending = order_ascending
        self.fiat = fiat
        self.headers = ["Date", "Open", "High", "Low", "Close", "Volume", "Market Cap"]
        self.rows = []
        self.proxies = proxies

        # enable all_time download if start_time or end_time is not given
        if not (self.start_date and self.end_date):
            self.all_time = True

        if not (self.all_time or (self.start_date and self.end_date)):
            raise InvalidParameters("'start_date' or 'end_date' cannot be empty if 'all_time' flag is False")


    def __repr__(self):
        return (
            "<CmcScraper coin_code:{}, start_date:{}, end_date:{}, all_time:{}>".format(self.coin_code, self.start_date, self.end_date, self.all_time)
        )

    def _download_data(self, **kwargs):
        """
        This method downloads the data.
        :param forced: (optional) if ``True``, data will be re-downloaded.
        :return:
        """

        forced = kwargs.get("forced")

        if self.rows and not forced:
            return

        if self.all_time:
            self.start_date, self.end_date = None, None

        coin_data = download_coin_data(self.coin_code, self.start_date, self.end_date, self.fiat, self.proxies)

        if coin_data:
            for _row in coin_data["data"]["quotes"]:
                _row_quote = list(_row["quote"].values())[0]
                date = datetime.strptime(
                    _row_quote["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).strftime("%d-%m-%Y")

                row = [date, _row_quote["open"], _row_quote["high"], _row_quote["low"], _row_quote["close"], _row_quote["volume"], _row_quote["market_cap"]]
                self.rows.insert(0, row)

            self.end_date, self.start_date = self.rows[0][0], self.rows[-1][0]

            if self.order_ascending:
                self.rows.sort(key=lambda x: datetime.strptime(x[0], "%d-%m-%Y"))

        else:
            pass

    def get_data(self, format="", verbose=False, **kwargs):
        """
        This method returns the downloaded data in specified format.
        :param format: extension name of data format. Available: json, xls, yaml, csv, dbf, tsv, html, latex, xlsx, ods
        :param verbose: (optional) Flag to enable verbose only.
        :param kwargs: Optional arguments that data downloader takes.
        :return:
        """

        self._download_data(**kwargs)
        if verbose:
            print(*self.headers, sep=", ")
            for row in self.rows:
                print(*row, sep=", ")

        elif format:
            data = tablib.Dataset()
            data.headers = self.headers
            for row in self.rows:
                data.append(row)
            return data.export(format)
        else:
            return self.headers, self.rows

    def get_dataframe(self, date_as_index=False, **kwargs):
        """
        This gives scraped data as DataFrame.
        :param date_as_index: make 'Date' as index and remove 'Date' column.
        :param kwargs: Optional arguments that data downloader takes.
        :return: DataFrame of the downloaded data.
        """

        try:
            import pandas as pd
        except ImportError:
            pd = None

        if pd is None:
            raise NotImplementedError(
                "DataFrame Format requires 'pandas' to be installed."
                "Try : pip install pandas"
            )

        self._download_data(**kwargs)

        dataframe = pd.DataFrame(data=self.rows, columns=self.headers)

        # convert 'Date' column to datetime type
        dataframe["Date"] = pd.to_datetime(
            dataframe["Date"], format="%d-%m-%Y", dayfirst=True
        )

        if date_as_index:
            # set 'Date' column as index and drop the the 'Date' column.
            dataframe.set_index("Date", inplace=True)

        return dataframe

    def export_csv(self, csv_name=None, csv_path=None, **kwargs):
        """
        This exports scraped data into a csv.
        :param csv_name: (optional) name of csv file.
        :param csv_path: (optional) path to where export csv file.
        :param kwargs: Optional arguments that data downloader takes.
        :return:
        """
        warnings.warn(
            "export_csv will be deprecated; Use 'export' method instead, e.g. export('csv')",
            PendingDeprecationWarning,
            stacklevel=2,
        )

        self._download_data(**kwargs)

        if csv_path is None:
            # Export in current directory if path not specified
            csv_path = os.getcwd()

        if csv_name is None:
            # Make name fo file in format of {coin_code}_{fiat}_{start_date}_{end_date}.csv
            csv_name = "{0}_{1}_{2}_{3}.csv".format(
                self.coin_code, self.fiat, self.start_date, self.end_date
            )

        if not csv_name.endswith(".csv"):
            csv_name += ".csv"

        _csv = "{0}/{1}".format(csv_path, csv_name)

        try:
            with open(_csv, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=",", quoting=csv.QUOTE_NONNUMERIC
                )
                writer.writerow(self.headers)
                for data in self.rows:
                    writer.writerow(data)
        except IOError as err:
            errno, strerror = err.args
            print("I/O error({0}): {1}".format(errno, strerror))

    def export(self, format, name=None, path=None, **kwargs):
        """
        Exports the data to specified file format
        :param format: extension name of file format. Available: json, xls, yaml, csv, dbf, tsv, html, latex, xlsx, ods
        :param name: (optional) name of file.
        :param path: (optional) output file path.
        :param kwargs: Optional arguments that data downloader takes.
        :return:
        """

        data = self.get_data(format, **kwargs)

        if path is None:
            # Export in current directory if path not specified
            path = os.getcwd()

        if name is None:
            # Make name of file in format: {coin_code}_{fiat}_{start_date}_{end_date}.csv
            name = "{0}_{1}-{2}_{3}".format(
                self.coin_code, self.fiat, self.start_date, self.end_date
            )

        if not name.endswith(".{}".format(format)):
            name += ".{}".format(format)

        _file = "{0}/{1}".format(path, name)

        try:
            with open(_file, "wb") as f:
                if type(data) is str:
                    f.write(data.encode("utf-8"))
                else:
                    f.write(data)
        except IOError as err:
            errno, strerror = err.args
            print("I/O error({0}): {1}".format(errno, strerror))
        except Exception as err:
            print("format: {0}, Error: {1}".format(format, err))
