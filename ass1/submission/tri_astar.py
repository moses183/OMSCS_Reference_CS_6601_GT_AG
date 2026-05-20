#####################################################
# CS 6601 - Assignment 1
# tri_astar.py
#####################################################

# DO NOT ADD OR REMOVE ANY IMPORTS FROM THIS FILE
import math
from submission.priority_queue import PriorityQueue
from submission.astar import euclidean_dist_heuristic

# Credits if any
# 1)
# 2)
# 3)

def custom_heuristic(graph, u, v):
    """
        Feel free to use this method to try and work with different heuristics and come up with a better search algorithm.
        Args:
            graph (ExplorableGraph): Undirected graph to search.
            u (str): Key for the first node to calculate from.
            v (str): Key for the second node to calculate to.
        Returns:
            Custom heuristic distance between `u` node and `v` node
        """
    return euclidean_dist_heuristic(graph, u, v)


def path_cost(graph, path):
    total_cost = 0
    for index in range(len(path) - 1):
        total_cost += graph.get_edge_weight(path[index], path[index + 1])
    return total_cost


def _a_star_path(graph, start, goal, heuristic):
    if start == goal:
        return []

    frontier = PriorityQueue()
    frontier.append((heuristic(graph, start, goal), (start, [start], 0)))
    best_cost = {start: 0}
    explored = set()

    while frontier.size() > 0:
        _, (node, path, cost) = frontier.pop()

        if node in explored:
            continue
        if cost > best_cost.get(node, float('inf')):
            continue
        if node == goal:
            return path

        explored.add(node)

        for neighbor in sorted(graph.neighbors(node)):
            if neighbor in explored:
                continue

            new_cost = cost + graph.get_edge_weight(node, neighbor)
            if new_cost < best_cost.get(neighbor, float('inf')):
                best_cost[neighbor] = new_cost
                priority = new_cost + heuristic(graph, neighbor, goal)
                frontier.append((priority, (neighbor, path + [neighbor], new_cost)))

    return []


def _oriented_path(graph, path_cache, start, goal, heuristic):
    if start == goal:
        return [start]
    if (start, goal) not in path_cache:
        path_cache[(start, goal)] = _a_star_path(graph, start, goal, heuristic)
    return path_cache[(start, goal)]


def _pair_key(first_index, second_index):
    if first_index < second_index:
        return first_index, second_index
    return second_index, first_index


def _stored_pair_path(paths_by_source, first_index, second_index, meeting_node):
    first_path = paths_by_source[first_index][meeting_node]
    second_path = paths_by_source[second_index][meeting_node]

    if first_index < second_index:
        return first_path + second_path[-2::-1]
    return second_path + first_path[-2::-1]


def _orient_pair_path(pair_paths, start_index, end_index):
    key = _pair_key(start_index, end_index)
    path = pair_paths[key]
    if start_index < end_index:
        return path
    return path[::-1]


def _best_three_goal_path(graph, pair_paths):
    candidates = PriorityQueue()
    goal_orders = [
        (0, 1, 2),
        (0, 2, 1),
        (1, 0, 2),
        (1, 2, 0),
        (2, 0, 1),
        (2, 1, 0),
    ]

    for start_index, middle_index, end_index in goal_orders:
        first_leg = _orient_pair_path(pair_paths, start_index, middle_index)
        second_leg = _orient_pair_path(pair_paths, middle_index, end_index)
        candidate_path = first_leg + second_leg[1:]
        candidates.append((path_cost(graph, candidate_path), candidate_path))

    return candidates.top()[1]


def _frontier_min_cost(frontier):
    if frontier.size() == 0:
        return float('inf')
    best_cost = float('inf')
    for _, (_, _, cost) in frontier:
        if cost < best_cost:
            best_cost = cost
    return best_cost


def _pair_searches_finished(pair_costs, frontiers):
    if len(pair_costs) < 3:
        return False

    top_costs = [_frontier_min_cost(frontier) for frontier in frontiers]
    for first_index in range(3):
        for second_index in range(first_index + 1, 3):
            key = _pair_key(first_index, second_index)
            if pair_costs[key] > top_costs[first_index] + top_costs[second_index]:
                return False
    return True


def _multi_goal_priority(graph, node, cost, source_index, goals, heuristic):
    estimates = []
    for index, goal in enumerate(goals):
        if index != source_index:
            estimates.append(heuristic(graph, node, goal))
    return cost + min(estimates)


def tridirectional_upgraded(graph, goals, heuristic=euclidean_dist_heuristic) -> list:
    """
    Exercise 4: Upgraded Tridirectional Search

    See README.MD for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        goals (list): Key values for the 3 goals
        heuristic: Function to determine distance heuristic.
            Default: euclidean_dist_heuristic.

    Returns:
        The best path as a list from one of the goal nodes (including both of
        the other goal nodes).
    """
    unique_goals = []
    for goal in goals:
        if goal not in unique_goals:
            unique_goals.append(goal)

    if len(unique_goals) == 1:
        return []
    if len(unique_goals) == 2:
        return _a_star_path(graph, unique_goals[0], unique_goals[1], heuristic)

    frontiers = []
    costs_by_source = []
    paths_by_source = []
    explored_by_source = []

    for index, goal in enumerate(unique_goals):
        frontier = PriorityQueue()
        priority = _multi_goal_priority(graph, goal, 0, index, unique_goals, heuristic)
        frontier.append((priority, (goal, [goal], 0)))
        frontiers.append(frontier)
        costs_by_source.append({goal: 0})
        paths_by_source.append({goal: [goal]})
        explored_by_source.append(set())

    pair_costs = {}
    pair_paths = {}

    while any(frontier.size() > 0 for frontier in frontiers):
        if _pair_searches_finished(pair_costs, frontiers):
            return _best_three_goal_path(graph, pair_paths)

        source_index = None
        source_priority = float('inf')
        for index, frontier in enumerate(frontiers):
            if frontier.size() > 0 and frontier.top()[0] < source_priority:
                source_index = index
                source_priority = frontier.top()[0]

        if source_index is None:
            break

        _, (node, path, cost) = frontiers[source_index].pop()
        if node in explored_by_source[source_index]:
            continue
        if cost > costs_by_source[source_index].get(node, float('inf')):
            continue

        explored_by_source[source_index].add(node)

        for other_index in range(3):
            if other_index == source_index:
                continue
            if node not in costs_by_source[other_index]:
                continue

            key = _pair_key(source_index, other_index)
            total_cost = cost + costs_by_source[other_index][node]
            if total_cost < pair_costs.get(key, float('inf')):
                pair_costs[key] = total_cost
                pair_paths[key] = _stored_pair_path(paths_by_source, source_index, other_index, node)

        for neighbor in sorted(graph.neighbors(node)):
            if neighbor in explored_by_source[source_index]:
                continue

            new_cost = cost + graph.get_edge_weight(node, neighbor)
            if new_cost < costs_by_source[source_index].get(neighbor, float('inf')):
                new_path = path + [neighbor]
                new_priority = _multi_goal_priority(graph, neighbor, new_cost,
                                                     source_index, unique_goals, heuristic)
                costs_by_source[source_index][neighbor] = new_cost
                paths_by_source[source_index][neighbor] = new_path
                frontiers[source_index].append((new_priority, (neighbor, new_path, new_cost)))

    if len(pair_paths) == 3:
        return _best_three_goal_path(graph, pair_paths)
    return []
