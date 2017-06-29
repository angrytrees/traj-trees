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
        predict only one trajectory
        :param trajectory: trajectory to predict
        :return: predicted value
        """
        if len(self.trees) == 0:
            print "The forest is empty"
            return -1
        
        tree_predictions = [] 
        
        
    def predict_one():
        print "predict one"
        
    def score():
        print "score is"