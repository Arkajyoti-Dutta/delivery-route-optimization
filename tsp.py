from graph import G
import networkx as nx

locations = ["Customer1", "Customer2", "Customer3"]

start = "Warehouse"

current = start

route = [start]

total_cost = 0

remaining = locations.copy()

while remaining:

    nearest = None
    min_cost = float('inf')

    for place in remaining:

        cost = nx.shortest_path_length(
            G,
            source=current,
            target=place,
            weight='weight'
        )

        if cost < min_cost:
            min_cost = cost
            nearest = place

    route.append(nearest)

    total_cost += min_cost

    current = nearest

    remaining.remove(nearest)

print("Optimized TSP Route:")
print(route)

print("Total Cost:", total_cost)