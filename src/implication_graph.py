import networkx as nx
import matplotlib.pyplot as plt

class ImplicationGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_implication(self, cause, effect):
        self.graph.add_edge(cause, effect)

    def visualize(self, filename='implication_graph.png'):
        plt.figure(figsize=(10, 7))
        nx.draw(self.graph, with_labels=True, node_color='lightblue', edge_color='gray')
        plt.title("Implication Graph")
        plt.savefig(filename)
        plt.close()
