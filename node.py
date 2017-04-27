# a Node class in a trajectory tree


class Node:
    def __init__(self):
        self.left = None  # the left child, if this value is None, the current node is a leaf
        self.right = None  # the right child

        # a list of indices of the trajectories kept at this node, only need to keep the indices,
        # not the actual trajectories to save space
        self.trajectory_idx = None

        # a list of indices of the starting points of the trajectories should be looked at for splitting the node
        self.starting_points_idx = None

        # a prediction worked at this node
        self.prediction = None

        # a decision point for this node (used for decision rule)
        self.decision_point = None

        # a decision radius for this node (used for decision rule)
        self.radius = None