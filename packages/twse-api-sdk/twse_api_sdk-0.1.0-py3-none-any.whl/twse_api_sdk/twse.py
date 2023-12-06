from typing import Optional
import requests

DEFAULT_ENDPOINT = "https://openapi.twse.com.tw/v1/"


class TwseV1:

    def __init__(self, endpoint=DEFAULT_ENDPOINT):
        self.endpoint = endpoint
        pass

    def list_monthly_operating_income(self):
        return requests.get(f"{self.endpoint}/opendata/t187ap05_P").json()

    def list_top_20_volume_stocks(self):
        return requests.get(f"{self.endpoint}/exchangeReport/MI_INDEX20").json()

    def list_day_trade_short_suspend_announcement(self):
        return requests.get(f"{self.endpoint}/exchangeReport/TWTBAU1").json()

    def list_day_trade_short_suspend_history(self):
        return requests.get(f"{self.endpoint}/exchangeReport/TWTBAU2").json()

    def get_per_5_sec_trading_volume(self):
        # The naming is wrong but provided by TWSE
        return requests.get(f"{self.endpoint}/exchangeReport/MI_5MINS").json()

    def list_top_20_oversea_holding_stocks(self):
        return requests.get(f"{self.endpoint}/fund/MI_QFIIS_sort_20").json()

    def list_oversea_holding_stock_industry_percentage_catagory(self):
        return requests.get(f"{self.endpoint}/fund​/MI_QFIIS_cat").json()

    def list_stock_pe_and_pb_and_dividend_yield(self):
        return requests.get(f"{self.endpoint}/exchangeReport/BWIBBU_ALL").json()

    def list_no_restriction_of_quota_change_stock(self):
        return requests.get(f"{self.endpoint}/exchangeReport/TWT88U").json()

    def list_stop_trading_stocks(self):
        return requests.get(f"{self.endpoint}/exchangeReport/TWTAWU").json()

    def list_stop_margin_stocks(self):
        return requests.get(f"{self.endpoint}/exchangeReport/BFI84U").json()

    def get_margin_volume(self):
        return requests.get(f"{self.endpoint}/exchangeReport/MI_MARGN").json()

    def get_abnormal_recommandated_stocks(self) -> Optional[dict]:
        res = requests.get(f"{self.endpoint}​/Announcement​/BFZFZU_T").json()
        if len(res) == 1 and res[0]["Code"] == "0":
            return None
        return res
