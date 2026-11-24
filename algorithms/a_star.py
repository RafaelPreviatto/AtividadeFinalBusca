import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distance = 0

        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue

            row, col = divmod(index, 3)

            goal_row, goal_col = divmod(tile - 1, 3)

            distance += abs(row - goal_row) + abs(col - goal_col)

        return distance

    def search(self, initial: State) -> SearchResult:
        frontier = []

        heapq.heappush(
            frontier, (initial.cost + self.heuristic(initial), initial)
        )

        visited = {initial: initial.cost}

        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            _, current = heapq.heappop(frontier)

            if current.cost > visited[current]:
                continue

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=len(current.path()) - 1
                )

            nodes_expanded += 1

            for neighbor in current.neighbors():
                if neighbor not in visited or neighbor.cost < visited[neighbor]:
                    visited[neighbor] = neighbor.cost

                    priority = neighbor.cost + self.heuristic(neighbor)

                    heapq.heappush(frontier, (priority, neighbor))

                    nodes_generated += 1

            max_frontier_size = max(
                max_frontier_size, len(frontier)
            )

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0
        )
