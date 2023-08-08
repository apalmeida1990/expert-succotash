import threading


class Counter:
    """
    A simple counter class that can be incremented and decremented.
    The initial goal was to make this thread-safe by handling the lock when incrementing and decrementing.
    But given my assumptions of the problem (i.e. When collection a fruit from a tree, no other farmer can collect from that tree), i feel that it was better to manage the locks at the process level.
    """

    def __init__(self, initial_value=0, name="Counter"):
        self.name = name
        self.value = initial_value
        self.lock = threading.Lock()

    def increment(self):
        # with self.lock:
        self.value += 1
        return self.value

    def decrement(self):
        # with self.lock:
        self.value -= 1
        return self.value

    def get_value(self):
        # with self.lock:
        return self.value
