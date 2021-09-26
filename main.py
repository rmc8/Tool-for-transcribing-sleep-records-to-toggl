import os
import sys

from pandas import DataFrame

from pkg.util import YamlConfig
from pkg.garmin import GarminAPI


def main():
    # Init
    dt_range: int = 0 if len(sys.argv) == 1 else int(sys.argv[1])
    yc = YamlConfig("./config.yml")
    settings: dict = yc.load()
    # toggl_token: str = settings["toggl"]["token"]
    env = os.environ
    garmin: dict = settings["garmin"]
    email: str = val if (val := env.get("GARMIN_EMAIL")) else garmin["email"]
    password: str = val if (val := env.get("GARMIN_PWD")) else garmin["password"]
    
    # Get sleep records from GarminAPI
    ga = GarminAPI(email=email, password=password)
    res: DataFrame = ga.get_sleep_logs(dt_range)
    print(res)


if __name__ == "__main__":
    main()
