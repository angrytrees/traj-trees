# a set of functions that builds a tree
from decision import find_decision_point, get_inside_outside_points
from node import Node
from tree import Tree


class TreeBuilding:
    def __init__(self):
        self.trajectories = list()  # a list of all trajectories in the database
        self.targets = list()  # a list of targets of the trajectories

    def split_node(self, node, max_radius, min_trajectories=1):
        """
        split a node
        :param node: a node in the tree
        :param max_radius: maximum radius in searching for decision point
        :param min_trajectories: minimum number of trajectories to split further
        :return:
        """
        if len(node.trajectory_idx) <= min_trajectories:
            # the node doesn't has enough trajectories to split, stop splitting
            return -1

        # get a set of starting points from the trajectories
        points = [self.trajectories[node.trajectory_idx[i]][node.starting_points_idx[i]] for i in range(len(node.starting_points_idx))]

        # get a set of targets
        targets = [self.targets[i] for i in range(len(node.trajectory_idx))]

        # find the best decision point and the best radius to split the points
        best_decision_point, best_radius = find_decision_point(points=points, targets=targets, max_radius=max_radius)

        inside, outside = get_inside_outside_points(best_decision_point, best_radius, points)

        # create the left child node:
        if len(inside) > 0:
            node.left = Node()
            node.left.trajectory_idx = [node.trajectory_idx[i] for i in inside]
            node.left.starting_point_idx = [node.starting_points_idx[i] + 1 for i in inside]

            # recursively split the left child
            self.split_node(node.left, max_radius, min_trajectories)

        # create the right child node:
        if len(outside) > 0:
            node.right = Node()
            node.right.trajectory_idx = [node.trajectory_idx[i] for i in outside]
            node.right.starting_point_idx = [node.starting_points_idx[i] + 1 for i in outside]

            # recursively split the right child
            self.split_node(node.right, max_radius, min_trajectories)

        return 1

    def initialize_tree(self):
        """
        initialize a tree with a root node
        :return: the initial tree
        """
        tree = Tree()
        # from the beginning all trajectories are kept at the root node
        tree.root.trajectory_idx = list(range(0,len(self.trajectories)))
        tree.root.starting_point_idx = [0]*len(self.trajectories)
        return tree

    def build_tree(self, max_radius, min_trajectories):
        # create the tree with initial root node
        tree = self.initialize_tree()
        self.split_node(tree.root, max_radius, min_trajectories)
        return tree






