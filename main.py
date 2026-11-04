import networkx as nx
import numpy as np

# RA
RA = "510267"
D1 = 5
D2 = 1
D3 = 0
D4 = 2
D5 = 6
D6 = 7

DESTINO = "S6"

# pesos
pesos = [                               
    ("S0", "S1", 10 + D6 % 5),             ("S0", "S2", 15 + D5 % 7),
    ("S1", "S2", 8 + D4 % 4),              ("S1", "S3", 12 + D3 % 6),
    ("S2", "S4", 14 + D2 % 5),             ("S2", "S5", 9 + D1 % 6),
    ("S3", "S4", 7 + (D5 + D6) % 5),       ("S3", "S6", 11 + (D4 + D5) % 6),
    ("S4", "S5", 6 + (D3 + D4) % 4),       ("S4", "S7", 16 + (D2 + D3) % 7),
    ("S5", "S7", 18 + (D1 + D2) % 8),      ("S6", "S7", 9 + (D5 + D1) % 5),
    ("S1", "S4", 20 + D6 % 4),
]

# pessos não negativos
assert all(p >= 0 for _, _, p in pesos), " tem pesos negativos"

# grafo
nos = ["S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7"]
grafo = nx.Graph()
grafo.add_nodes_from(nos)
grafo.add_weighted_edges_from(pesos)

# matriz de adjacência
matriz = nx.to_numpy_array(grafo, nodelist=nos, weight="weight", nonedge=np.nan)
print("Matriz de adjacência:")
print("      " + "".join(f"{n:>5}" for n in nos))
for i, linha in enumerate(matriz):
    print(f"{nos[i]:>5} " + "".join(f"{'—' if np.isnan(v) else int(v):>5}" for v in linha))

# dijkstra
custo, rota = nx.single_source_dijkstra(grafo, source="S0", target=DESTINO, weight="weight")
print(f"\nCusto mínimo S0 -> {DESTINO}: {custo}")
print("Rota:", " -> ".join(rota))

# antecessores e ordem de fechamento (a partir de S0)
pred, dist = nx.dijkstra_predecessor_and_distance(grafo, "S0", weight="weight")
ordem = sorted(nos, key=lambda n: (dist[n], nos.index(n)))
print("\nOrdem de fechamento:", " -> ".join(ordem))
print("Distancias:", ", ".join(f"{n}={dist[n]}" for n in ordem))
print("Antecessores:", ", ".join(f"{n}<-{pred[n][0]}" for n in nos if pred[n]))

# contingencia: queda do ramal e5 = (S2,S4)
cont = grafo.copy()
cont.remove_edge("S2", "S4")
custo_c, rota_c = nx.single_source_dijkstra(cont, source="S0", target=DESTINO, weight="weight")
print("\n--- Contingencia: queda do ramal e5 (S2,S4) ---")
print(f"Custo minimo S0 -> {DESTINO}: {custo_c}")
print("Rota:", " -> ".join(rota_c))
print(f"Acrescimo: {custo_c - custo} km ({(custo_c - custo) / custo * 100:.0f}%)")

# prim
print("\n--- Prim (MST) ---")
mst = nx.minimum_spanning_tree(grafo, algorithm="prim", weight="weight")
print("Arestas MST:", list(mst.edges(data="weight")))
print(f"Custo MST: {int(mst.size(weight='weight'))} km")


