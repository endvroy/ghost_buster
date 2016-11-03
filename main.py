from collections import deque, UserList
import copy
import heapq

tokens = {'-': 1,
          '|': 1,
          '^': 2,
          'v': 2,
          '%': 3}


def weight(token):
    return tokens[token]


class Ghost:
    def __init__(self, tokens):
        self.tokens = deque(tokens)
        self.weighed_sum = sum(weight(token) for token in self.tokens)

    def receive(self, token):
        if self.tokens[0] == token or token == '%':
            t = self.tokens.popleft()
            self.weighed_sum -= tokens[t]

    def busted(self):
        return not self.tokens


class SearchNode:
    def __init__(self, ghosts):
        self.ghosts = set(ghosts)
        self.steps = []

    def expand(self):
        available_tokens = {ghost.tokens[0] for ghost in self.ghosts}
        expanded = []
        for token in available_tokens:
            new_node = self.copy()
            for ghost in new_node.ghosts:
                ghost.receive(token)
            new_node.ghosts = {ghost for ghost in new_node.ghosts if not ghost.busted()}
            new_node.steps.append(token)
            expanded.append(new_node)
        return expanded

    def copy(self):
        return copy.deepcopy(self)

    def is_solution(self):
        return not self.ghosts


def h(node):
    return max(ghost.weighed_sum for ghost in node.ghosts)


def g(node):
    return sum(tokens[t] for t in node.steps)


def f(node):
    return g(node) + h(node)


class NodeSet(UserList):  # use a list to mimic a heap
    item_count = 0

    def add(self, node):
        heapq.heappush(self.data, (f(node), self.item_count, node))
        self.item_count -= 1

    def pop_most_promising(self):
        return heapq.heappop(self.data)[-1]

    def __iter__(self):
        return (x[-1] for x in self.data)


def backtrack(node_set):
    while node_set:
        node = node_set.pop_most_promising()  # choose the node
        expanded = node.expand()  # expand node
        if expanded:
            for x in expanded:
                if x.is_solution():  # check for solution
                    return x
                else:
                    node_set.add(x)
    else:
        return None


def solve(ghosts):
    node_set = NodeSet()
    node_set.add(SearchNode(ghosts))
    solution = backtrack(node_set)
    return solution


def print_solution(node):
    if node is None:
        print('no solution')
    else:
        print('optimal steps: {}'.format(node.steps))
        print('minimal cost: {}'.format(g(node)))


def main():
    ghosts = [Ghost('-|'),
              Ghost('^-'),
              Ghost('-^|-'),
              Ghost('v^%')]
    solution = solve(ghosts)
    print_solution(solution)


if __name__ == '__main__':
    main()
