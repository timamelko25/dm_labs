import networkx as nx
import matplotlib.pyplot as plt


def Floyd_Warshall(W, p, T, P):
    for i in range(p):
        for j in range(p):
            for k in range(p):
                T[i][j] = W[i][j]
                if W[i][j] == float('inf'):
                    P[i][j] = float('inf')
                else:
                    P[i][j] = i

    for i in range(p):
        for j in range(p):
            for k in range(p):
                if i != j and T[j][i] != float('inf') and i != k and T[i][k] != float('inf'):
                    if T[j][k] > T[j][i] + T[i][k]:
                        T[j][k] = T[j][i] + T[i][k]
                        P[j][k] = P[i][k]

    for j in range(p):
        if T[j][j] < 0:
            return -1


def reconstruct_paths(P, p):
    paths = [[None for _ in range(p)] for _ in range(p)]

    for i in range(p):
        for j in range(p):
            if i == j:
                paths[i][j] = [i]
            elif P[i][j] != float('inf'):
                path = []
                k = j
                while k != i:
                    path.append(k)
                    if P[i][k] == float('inf') or P[i][k] == k:
                        path = None
                        break
                    k = P[i][k]
                if path is not None:
                    path.append(i)
                    path.reverse()
                paths[i][j] = path
            else:
                paths[i][j] = None

    return paths




def save_matrix(matrix, filename):
    with open(filename, 'w') as file:
        for row in matrix:
            file.write(" ".join("{:8.3f}".format(col) if col != float('inf') else "inf" for col in row) + "\n")


def visualize_graph(W):
    G = nx.DiGraph()
    for i in range(len(W)):
        for j in range(len(W[i])):
            if W[i][j] != float('inf') and i != j:
                G.add_edge(i, j, weight=W[i][j])

    pos = nx.spring_layout(G)

    nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=10, font_weight='bold',
            arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    plt.show()


def main():
    num = 3
    with open(f'graph_{num}.txt', 'r') as file:
        W = []
        for line in file:
            row = []
            for value in line.strip().split():
                if value.lower() == 'inf':
                    row.append(float('inf'))
                else:
                    row.append(float(value))
            W.append(row)

    p = len(W)

    T = [[float('inf') for _ in range(p)] for _ in range(p)]
    P = [[float('inf') for _ in range(p)] for _ in range(p)]

    if Floyd_Warshall(W, p, T, P) == -1:
        print("отрицательный цикл.")
    else:
        save_matrix(T, f'T_{num}.txt')
        save_matrix(P, f'P_{num}.txt')
        paths = reconstruct_paths(P, p)
        for i in range(p):
            for j in range(p):
                print(f"Path from {i} to {j}: {paths[i][j]}")

    visualize_graph(W)

    return 0


if __name__ == "__main__":
    main()