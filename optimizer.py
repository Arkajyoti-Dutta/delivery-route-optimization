import osmnx as ox
import networkx as nx
from itertools import permutations
from geopy.geocoders import Nominatim


print("Loading Bhubaneswar road network...")

GLOBAL_GRAPH = ox.load_graphml(
    "bhubaneswar.graphml"
)

import time

print("Calculating bottleneck hubs...")

start = time.time()

centrality = nx.betweenness_centrality(
    GLOBAL_GRAPH,
    k=30,
    seed=42
)

print(
    f"Centrality calculation took {time.time()-start:.2f} seconds"
)

TOP_BOTTLENECKS = sorted(
    centrality.items(),
    key=lambda x: x[1],
    reverse=True
)[:5]

print("Bottleneck hubs ready.")

def get_bottleneck_hubs():

    hubs = []

    for node, score in TOP_BOTTLENECKS:

        lat = GLOBAL_GRAPH.nodes[node]["y"]
        lon = GLOBAL_GRAPH.nodes[node]["x"]

        try:

            location = geolocator.reverse(
                (lat, lon),
                exactly_one=True
            )

            address = location.raw["address"]

            area = (
                address.get("road")
                or address.get("suburb")
                or address.get("neighbourhood")
                or address.get("quarter")
                or address.get("city_district")
                or address.get("ward")
                or "Unknown Area"
            )

            if area not in hubs:
                hubs.append(area)

        except:

            hubs.append(
                f"({lat:.4f}, {lon:.4f})"
            )

       

    return hubs

print("Road network loaded.")


geolocator = Nominatim(
    user_agent="optiroute"
)


def optimize_route(
    warehouse,
    customer1,
    customer2,
    customer3,
    customer4,
    customer5
):

    # =========================
    # STORE FILLED LOCATIONS
    # =========================

    locations = [warehouse]

    customers = [
        customer1,
        customer2,
        customer3,
        customer4,
        customer5
    ]

    for customer in customers:

        if customer.strip() != "":
            locations.append(customer)

    
    if len(locations) < 2:

        raise Exception(
            "Please enter at least one customer location."
        )

    # =========================
    # GEOCODING
    # =========================

    coords = []

    for location in locations:

        try:

            latlng = ox.geocode(location)

            coords.append(latlng)

        except:

            raise Exception(
                f"Location not found: {location}"
            )

    # =========================
    # USE PRELOADED GRAPH
    # =========================

    G = GLOBAL_GRAPH

    # =========================
    # FIND NEAREST NODES
    # =========================

    nodes = []

    for lat, lon in coords:

        node = ox.distance.nearest_nodes(
            G,
            lon,
            lat
        )

        nodes.append(node)

        node_to_location = {}

        for i in range(len(nodes)): 


          node_to_location[nodes[i]] = locations[i]

        node_to_location = {}

        for i in range(len(nodes)):

            node_to_location[nodes[i]] = locations[i]

    customer_nodes = nodes[1:]

    all_routes = permutations(customer_nodes)

    # =========================
    # ROUTE CALCULATION
    # =========================

    best_distance = float("inf")

    best_route_nodes = None

    for route_order in all_routes:

        current_route = [nodes[0]] + list(route_order)

        current_distance = 0

        try:

            for i in range(len(current_route) - 1):

                current_distance += nx.shortest_path_length(
                    G,
                    current_route[i],
                    current_route[i + 1],
                    weight="length"
                )

            if current_distance < best_distance:

                best_distance = current_distance

                best_route_nodes = current_route

        except:

            continue

    if best_route_nodes is None:

        raise Exception(
            "Unable to find a road route between the selected " 
            "locations. Please try more specific locations within Bhubaneswar."
        )

    nodes = best_route_nodes

    best_route_order = []

    for node in best_route_nodes[1:]:

        best_route_order.append(
            node_to_location[node]
    )



    total_distance = best_distance

    segment_distances = []

    full_route = []

    for i in range(len(nodes) - 1):

        route = nx.shortest_path(
            G,
            nodes[i],
            nodes[i + 1],
            weight="length"
        )

        route_length = nx.shortest_path_length(
            G,
            nodes[i],
            nodes[i + 1],
            weight="length"
        )

        segment_distances.append(
            round(route_length / 1000, 2)
        )

        if len(full_route) == 0:

            full_route.extend(route)

        else:

            full_route.extend(route[1:])

    # =========================
    # DISTANCE & ETA
    # =========================

    total_distance_km = round(
        total_distance / 1000,
        2
    )

    eta = round(
        total_distance_km / 40,
        2
    )

    traffic_factor = 1.0

    if total_distance_km > 15:
        traffic_factor += 0.15

    predicted_eta = round( 
        eta * traffic_factor,
        2
    )

    # =========================
    # RETURN
    # =========================

    return (
        total_distance_km,
        eta,
        predicted_eta,
        segment_distances,
        best_route_order,
        best_route_nodes
)

