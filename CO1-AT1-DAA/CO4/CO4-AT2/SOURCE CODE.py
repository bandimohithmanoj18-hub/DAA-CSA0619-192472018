class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)

        if a == b:
            return False

        if self.rank[a] < self.rank[b]:
            a, b = b, a

        self.parent[b] = a

        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1

        return True


def kruskal(n, edges):
    edges.sort(key=lambda x: x[2])

    dsu = DSU(n)
    mst = []
    total_cost = 0

    for u, v, weight in edges:
        if dsu.union(u, v):
            mst.append((u, v, weight))
            total_cost += weight

            if len(mst) == n - 1:
                break

    if len(mst) != n - 1:
        return None, None

    return mst, total_cost


# Input
n = int(input("Enter number of cities: "))
m = int(input("Enter number of connections: "))

edges = []

print("Enter each connection as: city1 city2 cost")

for _ in range(m):
    u, v, w = map(int, input().split())
    edges.append((u, v, w))

# Find MST
mst, cost = kruskal(n, edges)

# Output
if mst is None:
    print("MST cannot be formed: graph is disconnected.")
else:
    print("\nSelected connections:")

    for u, v, w in mst:
        print(u, "-", v, ":", w)

    print("Minimum Network Cost =", cost)