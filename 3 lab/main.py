import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, filename):
        self.adj_matrix = self.read_adjacency_matrix(filename)
        self.V = len(self.adj_matrix)

    def read_adjacency_matrix(self, filename):
        with open(filename, 'r') as file:
            adj_matrix = [list(map(int, line.strip().split())) for line in file]
        return adj_matrix

    def find_cycle(self):
        visited = set()
        parent = {}
        cycle = []

        def dfs(vertex, prev):
            visited.add(vertex)
            parent[vertex] = prev
            for neighbor in range(self.V):
                if self.adj_matrix[vertex][neighbor] == 1:
                    if neighbor not in visited:
                        if dfs(neighbor, vertex):
                            return True
                    elif neighbor != prev:
                        nonlocal cycle
                        cycle = self.extract_cycle(vertex, neighbor, parent)
                        return True
            return False

        for vertex in range(self.V):
            if vertex not in visited:
                if dfs(vertex, -1):
                    return cycle
        return None

    def extract_cycle(self, start, end, parent):
        cycle = []
        while start != end:
            cycle.append(start)
            start = parent[start]
        cycle.append(end)
        cycle.append(cycle[0])
        cycle.reverse()
        return cycle

    def count_cycles(self):
        visited = set()
        cycle_count = 0

        def dfs(vertex, parent):
            nonlocal cycle_count
            visited.add(vertex)
            for neighbor in range(self.V):
                if self.adj_matrix[vertex][neighbor] == 1:
                    if neighbor not in visited:
                        dfs(neighbor, vertex)
                    elif neighbor != parent:
                        cycle_count += 1

        for vertex in range(self.V):
            if vertex not in visited:
                dfs(vertex, -1)
        return cycle_count // 2

    def is_connected(self):
        visited = set()

        def dfs(vertex):
            visited.add(vertex)
            for neighbor in range(self.V):
                if self.adj_matrix[vertex][neighbor] == 1 and neighbor not in visited:
                    dfs(neighbor)

        dfs(0)
        return len(visited) == self.V

    def is_acyclic(self):
        return self.find_cycle() is None

    def is_tree(self):
        return self.is_connected() and self.is_acyclic()

    def is_drevocislen(self):
        edge_count = sum(sum(row) for row in self.adj_matrix) // 2
        return edge_count == self.V - 1

    def is_subcyclic(self):
        cycle_count = self.count_cycles()
        if cycle_count > 1:
            return False, None
        for u in range(self.V):
            for v in range(self.V):
                if self.adj_matrix[u][v] == 0 and u != v:
                    self.adj_matrix[u][v] = 1
                    self.adj_matrix[v][u] = 1
                    num_cycles_after = self.count_cycles()
                    self.adj_matrix[u][v] = 0
                    self.adj_matrix[v][u] = 0
                    if num_cycles_after > 1:
                        return False, (u, v)
        return True, None

def visualize_graph(adj_matrix):
    G = nx.Graph()
    for i in range(len(adj_matrix)):
        for j in range(i, len(adj_matrix)):
            if adj_matrix[i][j] == 1:
                G.add_edge(i, j)
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(
        G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10, font_weight="bold"
    )
    plt.title("Graph Visualization")
    plt.show()

def main(filename):
    g = Graph(filename)
    print("Проверка свойств графа:")
    if g.is_acyclic():
        print("Граф является ацикличным.")
    else:
        cycle = g.find_cycle()
        print(f"Граф содержит цикл: {cycle}")
    if g.is_drevocislen():
        print("Граф является древочисленным (q = p - 1).")
    else:
        print("Граф не является древочисленным (q != p - 1).")
    is_subcyclic, edge = g.is_subcyclic()
    if is_subcyclic:
        print("Граф является субциклическим.")
    else:
        print(f"Субцикличность нарушена при добавлении ребра {edge}.")
    if g.is_tree():
        print("Граф является деревом.")
    else:
        print("Граф не является деревом.")
    visualize_graph(g.adj_matrix)

if __name__ == "__main__":
    main('graph_2.txt')
