import json
from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Sequence, Tuple

import mysql.connector
import requests
from ratelimit import limits, sleep_and_retry

# Set the rate limit to 5 calls per minute
from stock_api import StockAPI, StockData

AlphaVatangeRateLimiter = limits(calls=5, period=60)


class DataException(Exception):
    pass


class AlphaVantageDataStore:
    DATABASE_NAME = "stock_market"

    def __init__(self) -> None:
        # establish a local mysql connection
        self.mysql_connection = mysql.connector.connect(
            user="root",
            host="localhost",
            database=self.DATABASE_NAME,
        )

    def get_raw_data_for_symbol(self, symbol: str) -> Optional[Dict[str, Any]]:
        query = f"SELECT * FROM stock_data WHERE symbol = '{symbol}'"
        with self.mysql_connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result: Optional[Dict[str, Any]] = cursor.fetchone()  # type: ignore
            if not result:
                return None

            # convert json vals to dict
            for k, v in result.items():
                if k == "symbol":
                    continue
                result[k] = json.loads(v)
            return result

    def store_raw_data(self, raw_data: Dict[str, Any]) -> None:
        insert_stmt = "INSERT INTO stock_data SET " + ", ".join(
            ["{} = %s".format(k) for k in raw_data.keys()]
        )
        json_vals = [json.dumps(val) for val in list(raw_data.values())[1:]]
        with self.mysql_connection.cursor() as cursor:
            cursor.execute(insert_stmt, [raw_data["symbol"]] + json_vals)
            self.mysql_connection.commit()


class AlphaVantageAPI(StockAPI):
    API_KEY = "NU60T9FNG4BD8MKA"

    def __init__(self, data_store_class: type = AlphaVantageDataStore) -> None:
        self.data_store = data_store_class()

    def _find_reported_eps(self, earnings: List[Dict[str, str]], date: date) -> float:
        """
        Find the reported EPS at the given date. We find the earnings report that is directly
        before the specified date, and return the reported EPS for that report.
        Earnings report dates are in descending order
        """
        for earnings_report in earnings:
            earnings_date = datetime.strptime(
                earnings_report["fiscalDateEnding"], "%Y-%m-%d"
            ).date()
            if earnings_date <= date:
                return float(earnings_report["reportedEPS"])
        raise DataException("Could not find reported EPS")

    def _find_closest_date(self, target_date: date, price_dates: List[str]) -> date:
        closest_date: Optional[date] = None
        for price_date_str in price_dates:
            price_date = datetime.strptime(price_date_str, "%Y-%m-%d").date()
            if closest_date is None or abs(price_date - target_date) < abs(
                closest_date - target_date
            ):
                closest_date = price_date
        if closest_date is None:
            raise DataException("Could not find closest date")
        return closest_date

    def _convert_raw_data_to_stock_data(
        self, raw_data: Dict[str, Any], date: date
    ) -> StockData:
        symbol = raw_data["symbol"]
        prices = raw_data["prices"]
        earnings = raw_data["earnings"]
        company_info = raw_data["company_info"]

        # find the closest date to the target date
        price_dates = prices["Monthly Adjusted Time Series"]
        closest_date = self._find_closest_date(date, list(price_dates.keys()))
        closing_price = float(price_dates[str(closest_date)]["4. close"])

        reported_eps = self._find_reported_eps(earnings["quarterlyEarnings"], date)
        pe_ratio = closing_price / reported_eps

        last_year_date = date - timedelta(days=365)
        last_year_closest_date = self._find_closest_date(last_year_date, price_dates)
        last_year_price = float(price_dates[str(last_year_closest_date)]["4. close"])

        stock_data = StockData(
            symbol=symbol,
            date=date,
            price=closing_price,
            PE_ratio=pe_ratio,
            industry=company_info["Industry"],
            sector=company_info["Sector"],
            market_cap=float(company_info["MarketCapitalization"]),
            dividend_yield=float(company_info["DividendYield"]),
            last_year_price=last_year_price,
        )
        return stock_data

    def get_stock_data_for_symbol(self, symbol: str, date: date) -> StockData:
        raw_data = self.data_store.get_raw_data_for_symbol(symbol)
        if raw_data:
            stock_data = self._convert_raw_data_to_stock_data(raw_data, date)
        else:
            print(f"Fetching data for {symbol}...")
            prices = self.fetch_prices_for_symbol(symbol)
            earnings = self.fetch_earnings_for_symbol(symbol)
            company_info = self.fetch_company_info_for_symbol(symbol)
            raw_data = {
                "symbol": symbol,
                "prices": prices,
                "earnings": earnings,
                "company_info": company_info,
            }
            # convert to stock data first to ensure that the data is valid
            stock_data = self._convert_raw_data_to_stock_data(raw_data, date)
            self.data_store.store_raw_data(raw_data)

        return stock_data

    @sleep_and_retry  # type: ignore
    @AlphaVatangeRateLimiter  # type: ignore
    def fetch_prices_for_symbol(self, symbol: str) -> Dict[str, str]:
        prices_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={self.API_KEY}"
        return requests.get(prices_url).json()  # type: ignore

    @sleep_and_retry  # type: ignore
    @AlphaVatangeRateLimiter  # type: ignore
    def fetch_earnings_for_symbol(self, symbol: str) -> Dict[str, str]:
        earnings_url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={self.API_KEY}"
        return requests.get(earnings_url).json()  # type: ignore

    @sleep_and_retry  # type: ignore
    @AlphaVatangeRateLimiter  # type: ignore
    def fetch_company_info_for_symbol(self, symbol: str) -> Dict[str, str]:
        company_info_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={self.API_KEY}"
        return requests.get(company_info_url).json()  # type: ignore


print(
    AlphaVantageAPI().get_stock_data_for_symbol("IBM", date=date(2022, 12, 31)).__dict__
)
