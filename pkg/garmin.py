from datetime import date, datetime, timedelta

from garminconnect import Garmin

from pandas import DataFrame


class GarminAPI:
    def __init__(self, email: str, password: str, time_deff: int = -9):
        self.client = Garmin(email, password)
        self.client.login()
        self.time_deff: int = time_deff
    
    @staticmethod
    def epoc2date(epoc: int, time_deff: int):
        """
        Converts local epoch seconds to Datetime format
        :param epoc: Epoch Second (Local)
        :param time_deff: time difference
        :return: An object converted from epoch seconds to Datetime
                 type with time difference correction.
        """
        dt = datetime.fromtimestamp(epoc / 1000)
        return dt + timedelta(hours=time_deff)
    
    def get_sleep_logs(self, dt_range: int) -> DataFrame:
        """
        It retrieves sleep records in bulk and returns them in data frame format.
        :param dt_range: Enter the number of days to go back in the log (dt_range >= 0).
        :return: Data frame containing sleep time
        """
        table: list = []
        for dt_offset in range(dt_range + 1):
            print(dt_offset)
            tar_dt = (date.today() - timedelta(days=dt_offset))
            res: dict = self.client.get_sleep_data(tar_dt.isoformat())
            display: dict = res["dailySleepDTO"]
            if display.get("sleepStartTimestampLocal") and display.get("sleepEndTimestampLocal"):
                table.append({
                    "Date": tar_dt,
                    "sleepStart": self.epoc2date(display["sleepStartTimestampLocal"], self.time_deff),
                    "sleepEnd": self.epoc2date(display["sleepEndTimestampLocal"], self.time_deff),
                })
        return DataFrame(table)
