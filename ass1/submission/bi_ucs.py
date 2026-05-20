#####################################################
# CS 6601 - Assignment 1
# bi_ucs.py
#####################################################

# DO NOT ADD OR REMOVE ANY IMPORTS FROM THIS FILE
import math
from submission.priority_queue import PriorityQueue

# Credits if any
# 1)
# 2)
# 3)

def path_cost(graph, path):
    total_cost = 0
    for index in range(len(path) - 1):
        total_cost += graph.get_edge_weight(path[index], path[index + 1])
    return total_cost


def _merge_paths(forward_path, reverse_path):
    return forward_path + reverse_path[1:]


def bidirectional_ucs(graph, start, goal) -> list:
    """
    Exercise 1: Bidirectional Search.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start: Key for the start node.
        goal: Key for the end node.

    Returns:
        The best path via bi-UCS as a list from the start to the goal node (including both).
    """
    if start == goal:
        return []

    forward_frontier = PriorityQueue()
    reverse_frontier = PriorityQueue()
    forward_frontier.append((0, (start, [start], 0)))
    reverse_frontier.append((0, (goal, [goal], 0)))

    forward_costs = {start: 0}
    reverse_costs = {goal: 0}
    forward_paths = {start: [start]}
    reverse_paths = {goal: [goal]}
    forward_explored = set()
    reverse_explored = set()

    best_total = float('inf')
    best_path = []

    while forward_frontier.size() > 0 and reverse_frontier.size() > 0:
        forward_top = forward_frontier.top()[0]
        reverse_top = reverse_frontier.top()[0]

        if best_path and best_total <= forward_top + reverse_top:
            return best_path

        expand_forward = forward_top <= reverse_top
        expand_reverse = reverse_top <= forward_top

        if expand_forward and forward_frontier.size() > 0:
            _, (node, path, cost) = forward_frontier.pop()
            if node not in forward_explored and cost <= forward_costs.get(node, float('inf')):
                forward_explored.add(node)

                if node in reverse_costs:
                    total_cost = cost + reverse_costs[node]
                    if total_cost < best_total:
                        best_total = total_cost
                        best_path = _merge_paths(path, reverse_paths[node])

                for neighbor in sorted(graph.neighbors(node)):
                    if neighbor in forward_explored:
                        continue

                    new_cost = cost + graph.get_edge_weight(node, neighbor)
                    if new_cost < forward_costs.get(neighbor, float('inf')):
                        new_path = path + [neighbor]
                        forward_costs[neighbor] = new_cost
                        forward_paths[neighbor] = new_path
                        forward_frontier.append((new_cost, (neighbor, new_path, new_cost)))

                        if neighbor in reverse_costs:
                            total_cost = new_cost + reverse_costs[neighbor]
                            if total_cost < best_total:
                                best_total = total_cost
                                best_path = _merge_paths(new_path, reverse_paths[neighbor])

        if expand_reverse and reverse_frontier.size() > 0:
            _, (node, path, cost) = reverse_frontier.pop()
            if node not in reverse_explored and cost <= reverse_costs.get(node, float('inf')):
                reverse_explored.add(node)

                if node in forward_costs:
                    total_cost = cost + forward_costs[node]
                    if total_cost < best_total:
                        best_total = total_cost
                        best_path = _merge_paths(forward_paths[node], path)

                for neighbor in sorted(graph.neighbors(node)):
                    if neighbor in reverse_explored:
                        continue

                    new_cost = cost + graph.get_edge_weight(node, neighbor)
                    if new_cost < reverse_costs.get(neighbor, float('inf')):
                        new_path = [neighbor] + path
                        reverse_costs[neighbor] = new_cost
                        reverse_paths[neighbor] = new_path
                        reverse_frontier.append((new_cost, (neighbor, new_path, new_cost)))

                        if neighbor in forward_costs:
                            total_cost = new_cost + forward_costs[neighbor]
                            if total_cost < best_total:
                                best_total = total_cost
                                best_path = _merge_paths(forward_paths[neighbor], new_path)

    return best_path
