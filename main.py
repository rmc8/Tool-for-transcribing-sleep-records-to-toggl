import os
import sys
from datetime import datetime

from pandas import DataFrame

from pkg.util import YamlConfig
from pkg.garmin import GarminAPI
from pkg.toggl import TogglAPI


def main():
    # Init
    dt_range: int = 0 if len(sys.argv) == 1 else int(sys.argv[1])
    yc = YamlConfig("./config.yml")
    settings: dict = yc.load()
    env = os.environ
    
    # Garmin Settings
    garmin: dict = settings["garmin"]
    email: str = val if (val := env.get("GARMIN_EMAIL")) else garmin["email"]
    password: str = val if (val := env.get("GARMIN_PWD")) else garmin["password"]
    
    # toggle Settings
    toggl_token: str = val if (val := env.get("TOGGL_TOKEN")) else settings["toggl"]["token"]
    time_zone: int = val if (val := settings.get("time_zone")) else 9  # JST
    toggl_settings: dict = settings["toggl"]["time_entry"]
    
    # Get sleep records from GarminAPI
    ga = GarminAPI(email=email, password=password, time_deff=time_zone)
    res: DataFrame = ga.get_sleep_logs(dt_range)
    
    # Record your sleep time in toggl
    ta = TogglAPI(token=toggl_token)
    table: list = []
    for rec in res.to_dict(orient="records"):
        del rec["date"]
        rec.update(toggl_settings)
        res = ta.create_time_entry(**rec)
        table.append(res["data"])
    
    # Output log
    df = DataFrame(table)
    output_dir: str = "./output"
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(f"{output_dir}/toggl_res_{datetime.now():%Y%m%d_%H%M%S}.csv", index=False)


if __name__ == "__main__":
    main()
