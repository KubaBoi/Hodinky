import gtfs_kit as gk
import networkx as nx

feed = gk.feed.read_feed("test/PID_GTFS.zip", dist_units="km")

stop_a_name = "Hlavní nádraží"
stop_b_name = "Kněžská luka"

stop_a = feed.stops[feed.stops['stop_name'] == stop_a_name]
stop_b = feed.stops[feed.stops['stop_name'] == stop_b_name]

if stop_a.empty or stop_b.empty:
    print("Jedna nebo obě zastávky nebyly nalezeny.")
else:
    stop_a_id = stop_a.iloc[0]['stop_id']
    stop_b_id = stop_b.iloc[0]['stop_id']
    print(f"Stop A ID: {stop_a_id}, Stop B ID: {stop_b_id}")

    # Vytvoření prázdného grafu
    G = nx.DiGraph()

    # Přidání hran do grafu na základě spojů v GTFS
    for index, trip in feed.trips.iterrows():
        trip_id = trip['trip_id']
        trip_stops = feed.get_stops(trip_ids=[trip_id])
        #[stop["trip_id"] == trip_id for index, stop in feed.get_stop_times().iterrows()]
        for i in range(len(trip_stops) - 1):
            stop1 = trip_stops.iloc[i]
            stop2 = trip_stops.iloc[i + 1]
            G.add_edge(stop1['stop_id'], stop2['stop_id'], weight=stop2['arrival_time'] - stop1['departure_time'])

    # Použití Dijkstra's algoritmu k nalezení nejkratší cesty
    try:
        shortest_path = nx.shortest_path(G, source=stop_a_id, target=stop_b_id, weight='weight')
        print("Nejkratší trasa:", shortest_path)

        # Zobrazení názvů zastávek na trase
        for stop_id in shortest_path:
            stop_name = feed.stops[feed.stops['stop_id'] == stop_id].iloc[0]['stop_name']
            print(stop_name)

    except nx.NetworkXNoPath:
        print("Neexistuje žádná cesta mezi zastávkami.")
