class ForestBuilding:
    #def __init__(self):
    #    self.trajectories = list()  # a list of all trajectories in the database
    #    self.targets = list()  # a list of targets of the trajectories
    #    self.n_estimators = int() #the size of the forest
     
    def sample_traj(trajectories, targets, sample_share=0.66):
        """
        Random sample of trajectories and corresonding targets
        :param trajectories: list of trajectories
        :param targets: list of targets
        :param sample_share: share of sample size
        :return: list sampled trajectories and targets
        """
        sample_share = 0.66
        sample_size = int(len(targets) * sample_share)

        sample_idx = range(len(targets))
        sample_idx = random.sample(sample_idx, sample_size)

        sample_trajs = [trajectories[i] for i in sample_idx]
        sample_targets = [targets[i] for i in sample_idx]

        return sample_trajs, sample_targets
        
    def fit(self, trajectories, targets, n_estimators, sample_share, max_radius, min_trajectories):
        """
        Fit random forest
        :param trajectories: list of trajectories
        :param targets: list of targets
        :param n_estimators: the size of the forest
        :param sample_share: share of sample size
        :param max_radius: maximum radius in searching for decision point in trees
        :param min_trajectories: minimum number of trajectories to split further in trees
        :return: the builded forest
        """
        forest = Forest()
        
        for i in range(n_estimators):
            X_train, y_train = sample_traj(trajectories, targets, sample_share)

            clf = TreeBuilding()
            tree = clf.fit(X_train, y_train, max_radius, min_trajectories)
            forest.add(tree)
            
        return forest
            
        