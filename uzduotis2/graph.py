def min_distance(queue, dist):
    minimum = float("Inf")
    min_index = queue[0]

    for v in queue:
        if dist[v] < minimum:
            minimum = dist[v]
            min_index = v

    return min_index


class Graph:
    def __init__(self):
        self.adj_list = {}

    # Pridėti naują grafo vienkryptę briauną
    def add_edge(self, src, dst):
        if src not in self.adj_list:
            self.adj_list[src] = []
        self.adj_list[src].append(dst)

    # Trumpiausio kelio suradimas naudojant Dijkstra algoritmą.
    # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
    def shortest_path(self, src, dst):
        dist = {}
        prev = {}
        queue = []

        # Pridėti visas grafo viršūnes į eilę.
        for vertex in self.adj_list:
            dist[vertex] = float("Inf")
            prev[vertex] = None
            queue.append(vertex)

        # Kelio ilgis nuo pradinės viršūnės iki savęs pačios yra lygus 0.
        dist[src] = 0

        while queue:
            u = min_distance(queue, dist)
            queue.remove(u)

            # Jeigu randamas trumpiausias kelias iki dst, stabdyti kitų kelių paiešką.
            if u == dst:
                break

            for neighbor in self.adj_list[u]:
                if neighbor in queue:
                    alt = dist[u] + 1
                    if alt < dist[neighbor]:
                        dist[neighbor] = alt
                        prev[neighbor] = u

        # Sudaryti trumpiausio kelio seką nuo src iki dst.
        # Atvirkštinė tvarka, todėl viršūnės pridedamos į sekos pradžią.
        sequence = []
        u = dst
        if prev[u] or u == src:
            while u:
                sequence.insert(0, u)
                u = prev[u]

        return sequence
