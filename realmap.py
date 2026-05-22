import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

place = "Bhubaneswar, Odisha, India"

G = ox.graph_from_place(place, network_type='drive')

locations = {
    "Warehouse": "KIIT University, Bhubaneswar",
    "Customer1": "Bhubaneswar Railway Station",
    "Customer2": "Jaydev Vihar, Bhubaneswar",
    "Customer3": "Infocity, Bhubaneswar"
}

nodes = {}

for name, location in locations.items():

    point = ox.geocode(location)

    nearest_node = ox.distance.nearest_nodes(
        G,
        point[1],
        point[0]
    )

    nodes[name] = nearest_node

delivery_order = [
    "Warehouse",
    "Customer2",
    "Customer3",
    "Customer1"
]

total_distance = 0

for i in range(len(delivery_order) - 1):

    start = nodes[delivery_order[i]]

    end = nodes[delivery_order[i + 1]]

    route_length = nx.shortest_path_length(
        G,
        start,
        end,
        weight='length'
    )

    total_distance += route_length

print("Optimized Delivery Route:")
print(delivery_order)

print("Total Distance:", round(total_distance / 1000, 2), "km")

speed = 40

eta = (total_distance / 1000) / speed

print("Estimated Time:", round(eta, 2), "hours")

fig, ax = ox.plot_graph(
    G,
    bgcolor='black',
    node_size=0,
    edge_color='gray',
    edge_linewidth=0.5,
    show=False,
    close=False
)

for i in range(len(delivery_order) - 1):

    start = nodes[delivery_order[i]]

    end = nodes[delivery_order[i + 1]]

    route = nx.shortest_path(
        G,
        start,
        end,
        weight='length'
    )

    ox.plot_graph_route(
        G,
        route,
        route_color='red',
        route_linewidth=4,
        node_size=0,
        ax=ax,
        show=False,
        close=False
    )

    ax.set_title(
    "Smart Delivery Route Optimization",
    color='red',
    fontsize=16,
    pad=20
)
    
plt.show()