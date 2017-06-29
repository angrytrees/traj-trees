from node import Node
from decision import haversine
import numpy as np


class Tree:
    def __init__(self):
        self.root = Node()  # the root node of the tree

    def predict(self, trajectories):
        """
        predict the objective of requested trajectories
        :param trajectories: list of trajectories
        :return: list of predicted values
        """
        return [self.predict_one(trajectory) for trajectory in trajectories]

    def score(self, trajectories, targets):
        """
        Returns the mean haversine distance between the given and predicted targets
        :param trajectories: test trajectories samples
        :param targets: true targets
        :return: mean haversine distance between the given and predicted targets
        """
        predicted = self.predict(trajectories)
        return np.mean(np.power([haversine(targets[i], predicted[i]) for i in xrange(len(targets))], 2))

    def predict_one(self, trajectory):
        """
        predict only one trajectory
        :param trajectory: trajectory to predict
        :return: predicted value
        """
        current_node = self.root
       
        for idx, point in enumerate(trajectory):
            if len(trajectory) > (idx + 1):
                if (current_node.left == None) and (current_node.right == None):
                    prediction = current_node.prediction
                    
                elif (current_node.left == None) and (current_node.right != None):
                    current_node = current_node.right
                    
                elif (current_node.left != None) and (current_node.right == None):
                    current_node = current_node.left
                    
                else:
                    if haversine(point, current_node.decision_point) < current_node.radius:
                        current_node = current_node.left
                    else:
                        current_node = current_node.right
                        
            else:
                prediction = current_node.prediction
                
        return prediction