# a set of functions that builds a tree
from decision import find_decision_point, get_inside_outside_points
from node import Node
from tree import Tree
from error import SquareError


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

        print "length", len(node.trajectory_idx)
        if len(node.trajectory_idx) <= min_trajectories:
            # the node doesn't has enough trajectories to split, stop splitting
            return -1

        # get a list of starting points from the trajectories
        points = [self.trajectories[node.trajectory_idx[i]][node.starting_points_idx[i]] for i in range(len(node.trajectory_idx))]

        # get a list of targets
        targets = [self.targets[i] for i in range(len(node.trajectory_idx))]

        # find the best decision point and the best radius to split the points
        best_decision_point, best_radius = find_decision_point(points=points, targets=targets, max_radius=max_radius)

        # save decision point and radius
        node.decision_point = best_decision_point
        node.radius = best_radius

        inside, outside = get_inside_outside_points(best_decision_point, best_radius, points)

        # create the left child node:
        if len(inside) > 0:
            node.left = Node()
            # finding the prediction of the left node
            inside_targets = [targets[i] for i in inside]
            left_targets = SquareError()
            left_targets.add_list(inside_targets)
            node.left.prediction = left_targets.sum_of_square_error()
            del inside_targets, left_targets

            # we need to delete trajectories which are too short for next possible starting point id
            inside_without_short_traj = [i for i in inside if len(self.trajectories[node.trajectory_idx[i]]) > (node.starting_points_idx[i] + 1)]

            node.left.trajectory_idx  = [node.trajectory_idx[i] for i in inside_without_short_traj]
            node.left.starting_point_idx = [node.starting_points_idx[i] + 1 for i in inside_without_short_traj]

        # create the right child node:
        if len(outside) > 0:
            node.right = Node()
            # finding the prediction of the right node
            outside_targets = [targets[i] for i in outside]
            right_targets = SquareError()
            right_targets.add_list(outside_targets)
            node.right.prediction = right_targets.sum_of_square_error()
            del outside_targets, right_targets

            node.right.trajectory_idx = [node.trajectory_idx[i] for i in outside]
            node.right.starting_point_idx = [node.starting_points_idx[i] for i in outside]

        # trajectory_idx and starting_point_idx for this node won't be used anymore
        node.trajectory_idx = None
        node.starting_points_idx = None

        # recursively split the left child
        if len(inside_without_short_traj) > 0:
            self.split_node(node.left, max_radius, min_trajectories)

        # recursively split the right child
        if len(outside) > 0:
            self.split_node(node.right, max_radius, min_trajectories)

        return 1

    def initialize_tree(self, trajectories, targets):
        """
        initialize a tree with a root node
        :param trajectories: a list of all trajectories in the database
        :param targets: a list of targets of the trajectories
        :return: the initial tree
        """
        self.trajectories = trajectories
        self.targets = targets
        tree = Tree()
        # from the beginning all trajectories are kept at the root node
        tree.root.trajectory_idx = list(range(0,len(self.trajectories)))
        tree.root.starting_points_idx = [0]*len(self.trajectories)
        # finding the prediction of the root node
        root_points = SquareError()
        root_points.add_list(targets)
        tree.root.prediction = root_points.sum_of_square_error()
        del root_points
        return tree

    def build_tree(self, trajectories, targets, max_radius, min_trajectories):
        """
        create the tree with initial root node
        :param trajectories: a list of all trajectories in the database
        :param targets: a list of targets of the trajectories
        :param max_radius: maximum radius in searching for decision point
        :param min_trajectories: minimum number of trajectories to split further
        :return: the builded tree
        """
        tree = self.initialize_tree(trajectories, targets)
        self.split_node(tree.root, max_radius, min_trajectories)
        return tree






