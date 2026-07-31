from algoritmos.bellman_ford import bellman_ford_todos_os_pares
from algoritmos.dijkstra import dijkstra_todos_os_pares
from algoritmos.floyd_warshall import floyd_warshall
from algoritmos.johnson import johnson

ALGORITMOS = {
    "Bellman-Ford": bellman_ford_todos_os_pares,
    "Dijkstra": dijkstra_todos_os_pares,
    "Floyd-Warshall": floyd_warshall,
    "Johnson": johnson,
}

__all__ = ["ALGORITMOS"]
