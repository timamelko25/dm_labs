import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, filename):
        self.adj_matrix = self.read_matrix(filename)
        self.V = len(self.adj_matrix)

    def read_matrix(self, file_path):
        with open(file_path, 'r') as f:
            adj_matrix = [list(map(int, line.strip().split())) for line in f]
        return adj_matrix
    
    def write_answer(self, filename):
        filename = f'{filename}_answer.txt'
        with open(filename, 'w') as f:
            max_independent_set = self.find_max_independent_set()
            f.write(f"Наибольшее независимое множество вершин: {max_independent_set}")
            min_vertex_cover = list(set(range(self.V))-set(max_independent_set))
            f.write(f"Наименьшее вершинное покрытие: {min_vertex_cover}")

    def is_vertex_cover(self, vertex_set):
        edges = [(i, j) for i in range(self.V) for j in range(i + 1, self.V) if self.adj_matrix[i][j] == 1]
        for u, v in edges:
            if u not in vertex_set and v not in vertex_set:
                return False
        return True

    def is_independent_set(self, vertex_set):
        for i in vertex_set:
            for j in vertex_set:
                if i != j and self.adj_matrix[i][j] == 1:
                    return False
        return True

    def find_max_independent_set(self):
        global X, max_size
        X = []
        max_size = 0
        stack = []
        stack.append(([], list(range(self.V))))

        while stack:
            S, T = stack.pop()
            if len(S) > max_size:
                X = S[:]
                max_size = len(S)
            for v in T:
                if all(self.adj_matrix[v][u] == 0 for u in S):
                    new_T = [x for x in T if x != v]
                    stack.append((S + [v], new_T))
        return X

    def print_results(self):
        max_independent_set = self.find_max_independent_set()
        if self.is_independent_set(max_independent_set):
            print("Наибольшее независимое множество вершин:", max_independent_set)
        else:
            print("Полученное множество не является независимым")
        
        min_vertex_cover = list(set(range(self.V))-set(max_independent_set))
        if(self.is_vertex_cover(min_vertex_cover)):
            print("Наименьшее вершинное покрытие:", min_vertex_cover)
        else:
            print("Найдено не вершинное покрытие")

def visualize_graph(adj_matrix):
    G = nx.Graph()
    for i in range(len(adj_matrix)):
        for j in range(i, len(adj_matrix)):
            if adj_matrix[i][j] == 1:
                G.add_edge(i, j)
    all_vertices = set(range(len(adj_matrix)))
    connected_vertices = set(G.nodes())
    isolated_vertices = all_vertices - connected_vertices
    G.add_nodes_from(isolated_vertices)
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(
        G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10, font_weight="bold"
    )
    plt.title("Graph Visualization")
    plt.show()


if __name__ == "__main__":
    filename = "graph5.txt"
    graph = Graph(filename)
    graph.print_results()
    graph.write_answer(filename)
    visualize_graph(graph.adj_matrix)