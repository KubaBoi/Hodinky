import threading
from concurrent.futures import ThreadPoolExecutor
import networkx as nx


def get_data_dict(path: str, name: str) -> dict :
    with open(path, "r", encoding="utf-8") as f:
        dt = f.read()
    lines = dt.strip().split("\n")
    header = lines[0].split(",")
    data = {}
    for row in lines[1:]:
        values = row.split(",")
        rw = {}
        dict_name = None
        for i, h in enumerate(header):
            rw[h] = values[i]
            if (h == name):
                dict_name = values[i]
        data[dict_name] = rw
    return data

def load_stop_times(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        dt = f.read()
    lines = dt.strip().split("\n")
    header = lines[0].split(",")
    data = {}
    for row in lines[1:]:
        values = row.split(",")
        rw = {}
        for i, h in enumerate(header):
            rw[h] = values[i]
        if (rw["trip_id"] not in data.keys()):
            data[rw["trip_id"]] = []
        data[rw["trip_id"]].append(rw)
    return data

def get_data(path: str) -> list :
    """
    Create list of dictionaries from file at path. It takes first row for naming keys in dictionaries.
    """
    with open(path, "r", encoding="utf-8") as f:
        dt = f.read()
    lines = dt.strip().split("\n")
    header = lines[0].split(",")
    data = []
    for row in lines[1:]:
        values = row.split(",")
        rw = {}
        for i, h in enumerate(header):
            rw[h] = values[i]
        data.append(rw)
    return data

def find_items(data_set: list, key: str, value: str) -> list:
    data = []
    for item in data_set:
        if (item[key] == value):
            data.append(item)
    return data

def time_to_int(time: str) -> int:
    vals = time.split(":")
    return int(vals[2]) + (int(vals[1]) * 60) + (int(vals[0]) * 60 * 60)

def do_trip(trip: dict) -> None:
    trip_id = trip["trip_id"]
    trip_stops = stop_times[trip_id]
    for i in range(len(trip_stops) - 1):
        #print(find_items(stops, "stop_id", trip_stops[i]["stop_id"])[0]["stop_name"])
        stop1 = trip_stops[i]
        stop2 = trip_stops[i + 1]
        diff = time_to_int(stop2["arrival_time"]) - time_to_int(stop1["departure_time"])
        G.add_edge(stop1["stop_id"], stop2["stop_id"], weight=diff)

stops = get_data("test/files/stops.txt")
trips = get_data("test/files/trips.txt")
stop_times = load_stop_times("test/files/stop_times.txt")
print("Load done")

G = nx.DiGraph()
for trip in trips:
    do_trip(trip)
print("Graph done")

stop_a = find_items(stops, "stop_name", "\"Divadlo Gong\"")[0]
stop_b = find_items(stops, "stop_name", "\"Balabenka\"")[0]

shortest_path = nx.shortest_path(G, source=stop_a["stop_id"], target=stop_b["stop_id"], weight="weight")
print("Nejkratší trasa:", shortest_path)
