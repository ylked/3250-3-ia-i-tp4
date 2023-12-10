
class Node:
    def __init__(self, name, value, children=None):
        if children is None:
            children = []
        self.name = name
        self.value = value
        self.children = children

    def get_child(self, i):
        return self.children[i]

    def get_list_of_tuple_childen(self):
        ans = []
        for i in range(0, len(self.children)):
            ans.append((self.children[i], self.children[i].get_value()))
    def nb_children(self):
        return len(self.children)

    def get_value(self):
        return self.value

    def __str__(self):
        return f"Node {self.name}"


class Minimax:
    @staticmethod
    def get_max_tuple(tuples, is_max = 1):
        if len(tuples) < 1:
            return None
        max_tuple = tuples[0]
        for i in range(1,len(tuples)):
            if len(tuples[i]) != 2:
                return None
            if is_max * max_tuple[1] < is_max * tuples[i][1]:
                max_tuple = tuples[i]
        return max_tuple

    @staticmethod
    def choose_next_node(root, it, is_max):
        if root.nb_children() <= 0 or it <= 1:
            return root, root.get_value(),
        list_child = []
        for i in range(root.nb_children()):
            t = root.get_child(i), Minimax.choose_next_node(root.get_child(i), it-1, -is_max)[1]
            list_child.append(t)
        return Minimax.get_max_tuple(list_child, is_max)

if __name__ == "__main__":
    e100 = Node("100", 1)
    e8 = Node("8", 15)
    e9 = Node("9", 18)
    e7 = Node("7", 1, [e8, e9])
    e6 = Node("6", 2)
    e5 = Node("5", 3)
    e4 = Node("4", 10)
    e3 = Node("3", 4, [e6, e7])
    e0 = Node("0", 23)
    e2 = Node("2", 11, [e4, e5, e0])
    e1 = Node("1", 7, [e2, e3, e100])


    print(Minimax.choose_next_node(e1,5, 1)[0])