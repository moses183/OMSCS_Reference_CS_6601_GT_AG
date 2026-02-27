#####################################################
# CS 6601 - Assignment 0
# priority_queue.py
#####################################################
from heapq import heapify


# DO NOT ADD OR REMOVE ANY IMPORTS FROM THIS FILE

class MinHeap(object):
    def __init__(self):
        self.heap = []
        self.order_id = 0

    def heapify_up(self, pos):
        parent_pos = (pos-1) // 2
        if pos > 0 and self.heap[pos] < self.heap[parent_pos]:
            self.heap[pos], self.heap[parent_pos] = self.heap[parent_pos], self.heap[pos]
            self.heapify_up(parent_pos)

    def heapify_down(self, pos):
        left_child_pos = 2 * pos + 1
        right_child_pos = 2 * pos + 2
        smallest_child_pos = pos

        if left_child_pos < len(self.heap) and self.heap[left_child_pos] < self.heap[smallest_child_pos]:
            smallest_child_pos = left_child_pos

        if right_child_pos < len(self.heap) and self.heap[right_child_pos] < self.heap[smallest_child_pos]:
            smallest_child_pos = right_child_pos

        if smallest_child_pos != pos:
            self.heap[smallest_child_pos] , self.heap[pos] = self.heap[pos], self.heap[smallest_child_pos]
            self.heapify_down(smallest_child_pos)

    def insert(self, val):
        self.heap.append((val[0], self.order_id, val[1]))
        self.order_id += 1
        self.heapify_up(len(self.heap) - 1)

    def remove_min(self):
        if not self.heap:
            return None

        if len(self.heap) == 1:
            min_val=self.heap.pop()
            return min_val[0], min_val[2]


        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        min_val = self.heap.pop()

        self.heapify_down(0)

        return min_val[0], min_val[2]

    # def rem_node(self,value):
    #     for i , (prio, order_id, val) in enumerate(self.heap):
    #         if val == value[1]:
    #             self.heap[i]=self.heap.pop()
    #             if i < len(self.heap):
    #                 self.heapify_down(i)
    #                 self.heapify_up(i)
    #             return

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
    """

    def __init__(self):
        """Initialize a new Priority Queue."""

        self.queue = MinHeap()

    def pop(self):
        """
        Pop top priority node from queue.

        Returns:
            The node with the highest priority.
        """
        return self.queue.remove_min()

        # TODO: finish this function!
        #raise NotImplementedError

    def remove(self, node):
        """
        Remove a node from the queue.

        Hint: You might require this in ucs. However, you may
        choose not to use it or to define your own method.

        Args:
            node (tuple): The node to remove from the queue.
        """
        #self.queue.rem_node(node)
        # We will not test this function, implementation and desired behavior is up to your discretion
        # Some students find that this function is useful for them in Assignment 1
        #raise NotImplementedError
        newQueue = PriorityQueue()
        for n in self.queue.heap:

            if node[1] == n[2]:
                continue
            else:
                newQueue.append((n[0],n[2]))
        return newQueue



    def __iter__(self):
        """Queue iterator."""
        sort_elms= sorted([(n[0], n[2]) for n in self.queue.heap])
        return iter(sort_elms)

    def __str__(self):
        """Priority Queue to string."""

        return 'PQ:%s' % [(n[0], n[2]) for n in self.queue.heap]

    def pq_as_list(self):

        l=[]
        l2=[]
        for n in self.queue.heap:
            l.append(n[2])
            l2.append(n[0])
        return l,l2

    def append(self, node):
        """
        Append a node to the queue.

        Args:
            node (tuple): Comparable Object to be added to the priority queue.
            Provided in the form of (int priority, any type payload)
        """
        self.queue.insert(node)
        # TODO: finish this function!
        #raise NotImplementedError
        
    def __contains__(self, key):
        """
        Containment Check operator for 'in'

        Args:
            key: The key to check for in the queue.

        Returns:
            True if key is found in queue, False otherwise.
        """
        queue = [(n[0], n[2]) for n in self.queue.heap]
        return key in [n[-1] for n in queue]
        # return any(key == value for prior, order_id, value in self.queue.heap)

    def ele(self,key):
        #returns element from pq if it is in the pq
        e=None
        queue = [(n[0], n[2]) for n in self.queue.heap]
        for q in queue:
            if q[1] == key:
                e = q
                break
        return e


    def __eq__(self, other):
        """
        Compare this Priority Queue with another Priority Queue.

        Args:
            other (PriorityQueue): Priority Queue to compare against.

        Returns:
            True if the two priority queues are equivalent.
        """
        if not isinstance(other, PriorityQueue):
            return False
        curr_queue = [(n[0], n[2]) for n in self.queue.heap]
        other_queue = [(n[0], n[2]) for n in other.queue.heap]
        return curr_queue == other_queue

    def size(self):
        """
        Get the current size of the queue.

        Returns:
            Integer of number of items in queue.
        """

        return len(self.queue.heap)

    def clear(self):
        """Reset queue to empty (no nodes)."""

        self.queue.heap = []
        self.queue.order_id = 0

    def top(self):
        """
        Get the top item in the queue.

        Returns:
            The first item stored in the queue.

        """

        node = self.queue.heap[0]
        return node[0], node[2]
