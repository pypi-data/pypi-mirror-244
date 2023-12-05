import pandas as pd
from geopandas import GeoDataFrame, points_from_xy
from datetime import datetime, timedelta
import numpy as np
from uuid import uuid4

GAP1 = timedelta(hours=1)
GAP2 = timedelta(hours=8)
GAP3 = timedelta(hours=24)

def compute_gaps(gdf):
    gdf = __parse_features(gdf)
    return __gap_gdf(gdf)

def __gap_by_time(df, delta_time_min, delta_time_max, type_gap="Moderado"):
    if delta_time_max is not None:
        gap_or = df.loc[(df.next_msgdate >= delta_time_min) & (df.next_msgdate <= delta_time_max)]
    else:
        gap_or = df.loc[(df.next_msgdate >= delta_time_min)]

    gap_or["point_gap"] = "start"
    gap_or["id_gap"] = gap_or.apply(lambda x: str(uuid4()), axis=1)

    gap_dest = df.loc[gap_or.next_idx, :]
    gap_dest["point_gap"] = "end"
    gap_dest["id_gap"] = gap_dest["idx"].apply(lambda x: gap_or[gap_or.next_idx == x]["id_gap"].values[0])

    gap = pd.concat([gap_or, gap_dest], ignore_index=True)
    gap["type_gap"] = type_gap
    gap["secs_next_msg"] = gap["next_msgdate"].apply(lambda x: x / np.timedelta64(1, 's')).astype(int)
    gap["hs_next_msg"] = gap["next_msgdate"].apply(lambda x: round(x.total_seconds() / 60, 2))
    gap["time_gap"] = gap["next_msgdate"].apply(lambda x: str(x))

    return gap.drop(["next_idx", "next_msgdate"], axis=1)

def __get_speed_group(speed, step=2, max_value=12):
    speed_ranges = [(i, min(i+step, max_value)) for i in range(0, max_value, step)]

    for lower, upper in speed_ranges:
        if lower <= speed < upper:
            return f"{lower}-{upper} nudos"

    return f"> {max_value} nudos" if speed > max_value else "No reportada"

def __gap_gdf(gdf):
    gap_1hs = __gap_by_time(gdf, GAP1, GAP2, type_gap="Moderado")
    gap_8hs = __gap_by_time(gdf, GAP2, GAP3, type_gap="Grave")
    gap_24hs = __gap_by_time(gdf, GAP3, None, type_gap="Muy grave")
    gap = pd.concat([gap_1hs, gap_8hs, gap_24hs], ignore_index=True)

    gap_gdf = GeoDataFrame(
        gap, geometry=points_from_xy(gap["longitude"], gap["latitude"])
    )

    gap_gdf["speed_group"] = gap_gdf["speedovergroud"].apply(__get_speed_group)

    return gap_gdf

def __parse_features(df):
    df["msgdate"] = df["msgtime"].apply(lambda x: datetime.fromtimestamp(int(x/1000)))
    df = df.sort_values(by="msgdate").reset_index(drop=True)
    df = df.reset_index().rename(columns={"index": "idx"})

    df["next_msgdate"] = (df.groupby('mmsi')['msgdate'].shift(-1) - df['msgdate']).fillna(timedelta(hours=0))
    df["next_idx"] = df.groupby('mmsi')['idx'].shift(-1).fillna(0).astype(int)

    return df