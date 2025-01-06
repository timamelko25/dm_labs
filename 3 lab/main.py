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
    
    def write_matrix(self, filename):
        filename = f'{filename}_answer.txt'
        with open(filename, 'w') as f:
            if self.is_acyclic():
                f.write("Граф является ацикличным.")
            else:
                cycle = self.find_cycle()
                f.write(f"Граф содержит цикл: {cycle}")
            if self.is_drevocislen():
                f.write("Граф является древочисленным (q = p - 1).")
            else:
                f.write("Граф не является древочисленным (q != p - 1).")
            is_subcyclic, edge = self.is_subcyclic()
            if is_subcyclic:
                f.write("Граф является субциклическим.")
            else:
                f.write(f"Субцикличность нарушена при добавлении ребра {edge}.")
            if self.is_tree():
                f.write("Граф является деревом.")
            else:
                f.write("Граф не является деревом.")

    def find_cycle(self):
        visited = set()
        parent = {}
        cycle = []

        def dfs(start):
            stack = [(start, -1)]
            while stack:
                vertex, prev = stack.pop()
                if vertex not in visited:
                    visited.add(vertex)
                    parent[vertex] = prev
                    for neighbor in range(self.V):
                        if self.adj_matrix[vertex][neighbor] == 1:
                            if neighbor not in visited:
                                stack.append((neighbor, vertex))
                            elif neighbor != prev:
                                return self.extract_cycle(vertex, neighbor, parent)
            return None

        for vertex in range(self.V):
            if vertex not in visited:
                cycle = dfs(vertex)
                if cycle:
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
        all_cycles = set()
        for start in range(self.V):
            stack = [(start, [start], [False] * self.V)]
            while stack:
                current, path, visited = stack.pop()
                visited[current] = True
                for neighbor in range(self.V):
                    if self.adj_matrix[current][neighbor] == 1:
                        if neighbor == start and len(path) > 2:
                            cycle = tuple(sorted(path))
                            all_cycles.add(cycle)
                        elif not visited[neighbor]:
                            stack.append((neighbor, path + [neighbor], visited[:]))
                
                visited[current] = False 

        return len(all_cycles)


    def is_acyclic(self):
        return self.find_cycle() is None

    def is_tree(self):
        if self.is_acyclic() and self.is_subcyclic()[0]:
            return True

        return False

    def is_drevocislen(self):
        edge_count = sum(sum(row) for row in self.adj_matrix) / 2
        return edge_count == self.V - 1

    def is_subcyclic(self):
        max_cycles = -1
        for u in range(self.V):
            for v in range(self.V):
                if self.adj_matrix[u][v] == 0 and u != v:
                    self.adj_matrix[u][v] = 1
                    self.adj_matrix[v][u] = 1
                    num_cycles_after = self.count_cycles()
                    max_cycles = max(num_cycles_after, max_cycles)
                    self.adj_matrix[u][v] = 0
                    self.adj_matrix[v][u] = 0
                    if num_cycles_after > 1:
                        return False, (u, v)
        if max_cycles == 0:
            return False, None
        return True, None

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
    g.write_matrix(filename)
    
    visualize_graph(g.adj_matrix)

if __name__ == "__main__":
    main('graph_7.txt')
