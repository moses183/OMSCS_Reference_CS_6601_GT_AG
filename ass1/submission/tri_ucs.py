#####################################################
# CS 6601 - Assignment 1
# tri_ucs.py
#####################################################

# DO NOT ADD OR REMOVE ANY IMPORTS FROM THIS FILE
import math
from submission.priority_queue import PriorityQueue

# Credits if any
# 1) https://idm-lab.org/bib/abstracts/papers/ijcai20a.pdf
# 2)
# 3)

def path_cost(graph, path):
    total_cost = 0
    for index in range(len(path) - 1):
        total_cost += graph.get_edge_weight(path[index], path[index + 1])
    return total_cost


def _uniform_cost_path(graph, start, goal):
    if start == goal:
        return []

    frontier = PriorityQueue()
    frontier.append((0, (start, [start], 0)))
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
                frontier.append((new_cost, (neighbor, path + [neighbor], new_cost)))

    return []


def _oriented_path(graph, path_cache, start, goal):
    if start == goal:
        return [start]
    if (start, goal) not in path_cache:
        path_cache[(start, goal)] = _uniform_cost_path(graph, start, goal)
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


def _pair_searches_finished(graph, pair_costs, pair_paths, frontiers):
    if len(pair_costs) < 3:
        return False

    best_path = _best_three_goal_path(graph, pair_paths)
    best_total = path_cost(graph, best_path)

    top_costs = []
    for frontier in frontiers:
        if frontier.size() == 0:
            top_costs.append(float('inf'))
        else:
            top_costs.append(frontier.top()[0])

    pair_bounds = {}
    for first_index in range(3):
        for second_index in range(first_index + 1, 3):
            key = _pair_key(first_index, second_index)
            pair_bounds[key] = min(pair_costs[key], top_costs[first_index] + top_costs[second_index])

    lower_bound = min(
        pair_bounds[(0, 1)] + pair_bounds[(0, 2)],
        pair_bounds[(0, 1)] + pair_bounds[(1, 2)],
        pair_bounds[(0, 2)] + pair_bounds[(1, 2)],
    )
    return best_total <= lower_bound


def tridirectional_search(graph, goals) -> list:
    """
    Exercise 3: Tridirectional UCS Search

    See README.MD for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        goals (list): Key values for the 3 goals

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
        return _uniform_cost_path(graph, unique_goals[0], unique_goals[1])

    frontiers = []
    costs_by_source = []
    paths_by_source = []
    explored_by_source = []

    for goal in unique_goals:
        frontier = PriorityQueue()
        frontier.append((0, (goal, [goal], 0)))
        frontiers.append(frontier)
        costs_by_source.append({goal: 0})
        paths_by_source.append({goal: [goal]})
        explored_by_source.append(set())

    pair_costs = {}
    pair_paths = {}

    while any(frontier.size() > 0 for frontier in frontiers):
        if _pair_searches_finished(graph, pair_costs, pair_paths, frontiers):
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
                costs_by_source[source_index][neighbor] = new_cost
                paths_by_source[source_index][neighbor] = new_path
                frontiers[source_index].append((new_cost, (neighbor, new_path, new_cost)))

    if len(pair_paths) == 3:
        return _best_three_goal_path(graph, pair_paths)
    return []
