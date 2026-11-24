from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        frontier = [(initial, 0)]
        visited = {initial: 0}

        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            current, depth = frontier.pop()

            if depth > visited[current]:
                continue

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=depth
                )

            if depth >= self.depth_limit:
                continue

            nodes_expanded += 1

            for neighbor in reversed(current.neighbors()):
                new_depth = depth + 1

                if neighbor not in visited or new_depth < visited[neighbor]:
                    visited[neighbor] = new_depth
                    frontier.append((neighbor, new_depth))
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