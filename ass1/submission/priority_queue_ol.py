#####################################################
# CS 6601 - Assignment 1͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# priority_queue.py͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
#####################################################

# DO NOT ADD OR REMOVE ANY IMPORTS FROM THIS FILE͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
import math

# Credits if any͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 1)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 2)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# 3)͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃

class PriorityQueue(object):
    """
    A queue structure where each element is served in order of priority.
    Elements in the queue are popped based on the priority with higher priority
    elements being served before lower priority elements.  If two elements have
    the same priority, they will be served in the order they were added to the
    queue.
    Traditionally priority queues are implemented with heaps, but there are any
    number of implementation options.
    (Hint: take a look at the module heapq)
    You may add extra helper functions within the class if you find them necessary.
    Attributes:
        queue (list): Nodes added to the priority queue.

    Note:
        We have provided basic PQ implementation for you. You may find it helpful
        to tailor the implementation to your own usage (or to simply replace it with
        your implementation). This section will not be graded.
    """

    def __init__(self):
        """Initialize a new Priority Queue."""

        self.queue = []
        self.counter = 0 # FIFO Tracker

    def pop(self):
        """
        Pop top priority node from queue.
        Returns:
            The node with the highest priority.
        """

        if not self.queue:
            return None

        queue = self.queue
        top_node = queue[0][1]
        last_entry = queue.pop()

        if queue:
            queue_size = len(queue)
            current_index = 0

            while True:
                left_child = (2 * current_index) + 1
                if left_child >= queue_size:
                    break

                right_child = left_child + 1
                better_child = left_child

                if right_child < queue_size:
                    left_order, left_node = queue[left_child]
                    right_order, right_node = queue[right_child]
                    if (right_node[0], right_order) < (left_node[0], left_order):
                        better_child = right_child

                child_order, child_node = queue[better_child]
                last_order, last_node = last_entry
                if (last_node[0], last_order) <= (child_node[0], child_order):
                    break

                queue[current_index] = queue[better_child]
                current_index = better_child

            queue[current_index] = last_entry

        return top_node

    def remove(self, node):
        """
        Remove a node from the queue.
        Hint: You might require this in ucs. However, you may
        choose not to use it or to define your own method.
        Args:
            node (tuple): The node to remove from the queue.
        """
        
        # We will not test this function, implementation and desired behavior is up to your discretion͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
        # Some students find that this function is useful for them in Assignment 1͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
        raise NotImplementedError

    def __iter__(self):
        """Queue iterator."""

        return iter(sorted(self.queue))

    def __str__(self):
        """Priority Queue to string."""

        return 'PQ:%s' % self.queue

    def append(self, node):
        """
        Append a node to the queue.
        Args:
            node (tuple): Comparable Object to be added to the priority queue.
            Provided in the form of (int priority, any type payload)
        """

        entry = (self.counter, node)
        self.counter += 1
        queue = self.queue
        queue.append(entry)

        child_index = len(queue) - 1
        entry_order, entry_node = entry
        while child_index > 0:
            parent_index = (child_index - 1) // 2
            parent_order, parent_node = queue[parent_index]
            if (entry_node[0], entry_order) >= (parent_node[0], parent_order):
                break

            queue[child_index] = queue[parent_index]
            child_index = parent_index

        queue[child_index] = entry

    def __contains__(self, key):
        """
        Containment Check operator for 'in'
        Args:
            key: The key to check for in the queue.
        Returns:
            True if key is found in queue, False otherwise.
        """

        return key in [n[-1] for n in self.queue]

    def __eq__(self, other):
        """
        Compare this Priority Queue with another Priority Queue.
        Args:
            other (PriorityQueue): Priority Queue to compare against.
        Returns:
            True if the two priority queues are equivalent.
        """

        return self.queue == other.queue

    def size(self):
        """
        Get the current size of the queue.
        Returns:
            Integer of number of items in queue.
        """

        return len(self.queue)

    def clear(self):
        """Reset queue to empty (no nodes)."""

        self.queue = []

    def top(self):
        """
        Get the top item in the queue.
        Returns:
            The first item stored in the queue.
        """

        return self.queue[0][1]
    
    def swap(self, a, b):
        """
        Swaps two nodes in the queue given their indices
        """

        tmp = self.queue[a]
        self.queue[a] = self.queue[b]
        self.queue[b] = tmp

    def compare(self, a, b):
        """
        Compare two nodes in queue given their indices
        
        Returns:
            True if queue[a].priority < queue[b].priority
            True if queue[a].priority == queue[b].priority and queue[a].FIFO < queue[b].FIFO
            False otherwise
            Means queue[a] has higher priority than queue[b]
        """

        order_a, node_a = self.queue[a]
        order_b, node_b = self.queue[b]
        priority_a = node_a[0]
        priority_b = node_b[0]

        return (priority_a, order_a) < (priority_b, order_b)