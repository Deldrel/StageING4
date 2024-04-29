import tkinter as tk
from tkinter import simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from typing import Any, Tuple, List, Optional, Dict


def create_random_graph(number_of_nodes: int, number_of_edges: int, directed: bool = True) -> nx.DiGraph:
    """ Generate a random directed graph with specified attributes on edges. """
    graph = nx.gnm_random_graph(number_of_nodes, number_of_edges, directed=directed)
    for u, v in graph.edges():
        graph.edges[u, v]['distance'] = random.randint(10, 100)
        graph.edges[u, v]['carbon_footprint'] = random.randint(1, 100)
        graph.edges[u, v]['air_quality'] = random.randint(1, 100)
        graph.edges[u, v]['physical_activity'] = random.randint(1, 100)
    return graph


def get_attribute_color_list(graph: nx.Graph, attribute: str) -> List[Tuple[float, float, float, float]]:
    """ Get colors for edges based on the selected attribute. """
    color_list = []
    for u, v in graph.edges():
        value = graph.edges[u, v][attribute]
        color = (0, 0, 0, value / 100) if attribute == 'carbon_footprint' else (
        0, 1, 0, value / 100) if attribute == 'air_quality' else (
        1, 0, 0, value / 100) if attribute == 'physical_activity' else (0, 0, 0, 1)
        color_list.append(color)
    return color_list


def draw_graph(graph: nx.Graph, pos: Dict[Any, Tuple[float, float]], canvas: FigureCanvasTkAgg, state: Dict,
               attribute: str = 'distance', path: Optional[List[int]] = None) -> None:
    """ Draw or redraw the entire graph with selected start and end nodes highlighted. """
    plt.clf()
    edge_colors = get_attribute_color_list(graph, attribute)
    node_colors = ['green' if n == state['start_node'] else 'magenta' if n == state['end_node'] else 'gray' for n in graph.nodes()]
    # Dynamically adjust node size for visual representation
    node_sizes = [500 if n in [state['start_node'], state['end_node']] else 300 for n in graph.nodes()]
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=node_sizes)
    nx.draw_networkx_edges(graph, pos, edge_color=edge_colors)
    if path:
        nx.draw_networkx_edges(graph, pos, edgelist=list(zip(path, path[1:])), edge_color='blue', width=3)
    canvas.draw()



def main() -> None:
    root = tk.Tk()
    root.title("Graph Attributes Visualizer")
    root.protocol("WM_DELETE_WINDOW", root.quit)

    state = {'start_node': None, 'end_node': None, 'attribute': 'distance', 'node_radius': 0.05}
    graph = create_random_graph(10, 15)
    pos = nx.spring_layout(graph, weight='distance')

    fig, ax = plt.subplots(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    label_var = tk.StringVar(value="Use left click to select start node, right click for end node.")
    label = tk.Label(root, textvariable=label_var)
    label.pack(side=tk.BOTTOM)

    def update_graph(attribute: str = None) -> None:
        """ Update the graph drawing based on the current state and attribute. """
        if attribute:
            state['attribute'] = attribute
        draw_graph(graph, pos, canvas, state, state['attribute'])

    def on_click(event, button):
        """ Handle node selection based on mouse clicks. """
        node = next((n for n in graph if
                     ((pos[n][0] - event.xdata) ** 2 + (pos[n][1] - event.ydata) ** 2) ** 0.5 < state['node_radius']),
                    None)
        if node is not None:
            if button == 1:  # Left click for start node
                state['start_node'] = node
            elif button == 3:  # Right click for end node
                state['end_node'] = node
            update_graph()

    fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, event.button))

    def find_path() -> None:
        """ Compute and display the shortest path based on the selected nodes and attribute. """
        if state['start_node'] is not None and state['end_node'] is not None:
            try:
                path = nx.shortest_path(graph, source=state['start_node'], target=state['end_node'],
                                        weight=state['attribute'])
                draw_graph(graph, pos, canvas, state, state['attribute'], path)
            except nx.NetworkXNoPath:
                label_var.set("No path found between selected nodes.")
            except Exception as e:
                label_var.set(f"Error: {str(e)}")
        else:
            label_var.set("Select both start and end nodes.")

    def new_graph() -> None:
        """ Generate a new graph based on user inputs for nodes and edges. """
        num_nodes = simpledialog.askinteger("Number of Nodes", "Enter number of nodes:", parent=root, minvalue=2,
                                            maxvalue=100)
        num_edges = simpledialog.askinteger("Number of Edges", "Enter number of edges:", parent=root, minvalue=1,
                                            maxvalue=num_nodes * (num_nodes - 1))
        if num_nodes and num_edges:
            nonlocal graph, pos
            graph = create_random_graph(num_nodes, num_edges)
            pos = nx.spring_layout(graph, weight='distance')
            update_graph()

    # GUI elements for graph control
    tk.Button(root, text="New Graph", command=new_graph).pack(side=tk.LEFT)
    tk.Button(root, text="Compute Shortest Path", command=find_path).pack(side=tk.LEFT)

    for attribute in ["distance", "carbon_footprint", "air_quality", "physical_activity"]:
        tk.Button(root, text=attribute, command=lambda attr=attribute: update_graph(attr)).pack(side=tk.RIGHT)

    update_graph('distance')  # Initial drawing with 'distance'
    root.mainloop()


if __name__ == "__main__":
    main()
