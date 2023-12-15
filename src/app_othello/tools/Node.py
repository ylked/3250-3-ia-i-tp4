class Node:
    def __init__(self, name, value, children=None):
        if children is None:
            children = []
        self.name = name
        self.value = value
        self.children = children

    def get_child(self, i):
        return self.children[i]

    def get_list_of_tuple_children(self):
        ans = []
        for i in range(0, len(self.children)):
            ans.append((self.children[i], self.children[i].get_value()))
    def nb_children(self):
        return len(self.children)

    def get_value(self):
        return self.value

    def __str__(self):
        return f"Node {self.name}"