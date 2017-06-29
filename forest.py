import numpy as np
from decision import haversine

class Forest:
    def __init__(self):
        self.trees = list()  # the root node of the tree
        
    def add(self, tree):
        """
        Add new tree to forest
        :param tree: a trajectory tree
        :return: None
        """
        self.trees.append(tree)
        
    def predict(self, trajectories):
        """
        predict the objective of requested trajectories
        :param trajectories: list of trajectories
        :return: list of predicted values
        """
        if len(self.trees) == 0:
            print "The forest is empty"
            return -1
        
        tree_predictions = np.array([tree.predict(trajectories) for tree in self.trees])

        return [list(np.mean(tree_predictions[:,i], axis = 0)) for i in range(len(trajectories))]
        
    def score(self, trajectories, targets):
        """
        Returns the mean haversine distance between the given and predicted targets
        :param trajectories: test trajectories samples
        :param targets: true targets
        :return: mean haversine distance between the given and predicted targets
        """
        predicted = self.predict(trajectories)
        return np.mean(np.power([haversine(targets[i], predicted[i]) for i in xrange(len(targets))], 2))