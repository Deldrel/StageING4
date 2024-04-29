import osmnx as ox
import networkx as nx
from typing import List

ox.settings.use_cache = True
ox.settings.log_console = True


def plot_graph(graph: nx.MultiDiGraph) -> None:
    ox.plot_graph(graph, node_size=0, edge_linewidth=1, show=True)


def plot_graphs(graphs: List[nx.MultiDiGraph]) -> None:
    color_list = ["blue", "red", "green", "yellow", "purple", "orange", "pink", "brown", "black", "gray"]
    for i, graph in enumerate(graphs):
        color = color_list[i]
        gdf_nodes, gdf_edges = ox.graph_to_gdfs(graph, nodes=True, edges=True)
        if i == 0:
            map = gdf_edges.explore(color=color, show=False)
        else:
            gdf_edges.explore(m=map, color=color, show=False)
    map.save("map.html")


def fetch_walkways(city: str) -> nx.MultiDiGraph:
    custom_filter = '["footway"]'
    graph = ox.graph_from_place(city, custom_filter=custom_filter)
    return graph


def fetch_bike_lanes(city: str) -> nx.MultiDiGraph:
    custom_filter = '["cycleway"]'
    graph = ox.graph_from_place(city, custom_filter=custom_filter)
    return graph


def fetch_non_wheelchair_friendly(city: str) -> nx.MultiDiGraph:
    custom_filter = '["highway"]["wheelchair"="no"]'
    graph = ox.graph_from_place(city, custom_filter=custom_filter)
    return graph


def main() -> None:
    city = "Lyon, France"
    walkways = fetch_walkways(city)
    bike_lanes = fetch_bike_lanes(city)
    non_wheelchair_friendly = fetch_non_wheelchair_friendly(city)
    plot_graphs([walkways, bike_lanes, non_wheelchair_friendly])

    print(f"Graphs for {city} fetched and saved to map.html, more information below.")
    print(f"Walkways graph: {walkways}")
    print(f"Bike lanes graph: {bike_lanes}")
    print(f"Non wheelchair friendly graph: {non_wheelchair_friendly}")


if __name__ == "__main__":
    main()
