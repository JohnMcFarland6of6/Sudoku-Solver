class Node():
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None

class DoubleLinkedList():
    def __init__(self, node=None):
        self.head = node
        self.tail = node
        self.current = node

    def addTail(self, node):
        if self.head == None:
            self.head = node
            self.tail = node
            self.current = node
        else:
            node.prev = self.tail
            node.prev.next = node
            self.tail = node