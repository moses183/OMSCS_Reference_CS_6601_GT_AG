#####################################################
# CS 6601 - Assignment 1͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# bi_astar.py͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
#####################################################

# DO NOT ADD OR REMOVE ANY IMPORTS FROM THIS FILE͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
import math


from submission.priority_queue import PriorityQueue
from submission.astar import euclidean_dist_heuristic

# Credits if any͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 1)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 2)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 3)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃

def null_heuristic(graph, u, v):

    return 0

def path_cost(graph, path):
    total_cost = 0
    for index in range(len(path) - 1):
        total_cost += graph.get_edge_weight(path[index], path[index + 1])
    return total_cost


def euclidean_dist_heuristic(graph, u, v):

    ux, uy = graph.nodes[u]['pos']
    vx, vy = graph.nodes[v]['pos']
    return round(math.hypot(vx - ux, vy - uy), 3)

def _smallest_edge_weight(graph):
    smallest_weight = float('inf')
    for edge in graph.edges:
        edge_weight = graph.get_edge_weight(edge[0], edge[1])
        if edge_weight < smallest_weight:
            smallest_weight = edge_weight
    return 0 if smallest_weight == float('inf') else smallest_weight


def _priority(graph, cost_so_far, node, target, epsilon, heuristic=euclidean_dist_heuristic):
    estimated_total = cost_so_far + heuristic(graph, node, target)
    balanced_total = (2 * cost_so_far) + epsilon
    return max(estimated_total, balanced_total)


def _merge_paths(forward_path, reverse_path):
    return forward_path + reverse_path[1:]

def bidirectional_a_star(graph, start, goal, heuristic=euclidean_dist_heuristic) -> list:
    """
    Exercise 2: Bidirectional A*.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start: Key for the start node.
        goal: Key for the end node.
        heuristic: Function to determine distance heuristic.
            Default: euclidean_dist_heuristic.

    Returns:
        The best path via bi-A* as a list from the start to the goal node (including both).
    """
    if start == goal:
        return []

    epsilon = _smallest_edge_weight(graph)

    forward_frontier = PriorityQueue()
    reverse_frontier = PriorityQueue()
    forward_start_priority = _priority(graph, 0, start, goal, epsilon, heuristic)
    reverse_start_priority = _priority(graph, 0, goal, start, epsilon, heuristic)
    forward_frontier.append((forward_start_priority, (start, [start], 0)))
    reverse_frontier.append((reverse_start_priority, (goal, [goal], 0)))

    forward_costs = {start: 0}
    reverse_costs = {goal: 0}
    forward_paths = {start: [start]}
    reverse_paths = {goal: [goal]}
    forward_explored = set()
    reverse_explored = set()

    best_total = float('inf')
    best_path = []

    while forward_frontier.size() > 0 and reverse_frontier.size() > 0:
        forward_priority, (forward_node, _, forward_cost) = forward_frontier.top()
        reverse_priority, (reverse_node, _, reverse_cost) = reverse_frontier.top()
        smaller_priority = min(forward_priority, reverse_priority)

        forward_estimate = forward_cost + heuristic(graph, forward_node, goal)
        reverse_estimate = reverse_cost + heuristic(graph, reverse_node, start)
        lower_bound = max(smaller_priority, forward_estimate, reverse_estimate,
                          forward_cost + reverse_cost + epsilon)

        if best_path and best_total <= lower_bound:
            return best_path

        expand_forward = forward_priority < reverse_priority
        expand_reverse = reverse_priority <= forward_priority

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
                        new_priority = _priority(graph, new_cost, neighbor, goal, epsilon, heuristic)
                        forward_costs[neighbor] = new_cost
                        forward_paths[neighbor] = new_path
                        forward_frontier.append((new_priority, (neighbor, new_path, new_cost)))

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
                        new_priority = _priority(graph, new_cost, neighbor, start, epsilon, heuristic)
                        reverse_costs[neighbor] = new_cost
                        reverse_paths[neighbor] = new_path
                        reverse_frontier.append((new_priority, (neighbor, new_path, new_cost)))

                        if neighbor in forward_costs:
                            total_cost = new_cost + forward_costs[neighbor]
                            if total_cost < best_total:
                                best_total = total_cost
                                best_path = _merge_paths(forward_paths[neighbor], new_path)

    return best_path
