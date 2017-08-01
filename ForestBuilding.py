from forest import Forest
from build import TreeBuilding
import multiprocessing as mp
import copy_reg
import types
import random

def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)

class ForestBuilding:
    #def __init__(self):
    #    self.trajectories = list()  # a list of all trajectories in the database
    #    self.targets = list()  # a list of targets of the trajectories
    #    self.n_estimators = int() #the size of the forest
     
    def sample_traj(self, trajectories, targets, sample_share):
        """
        Random sample of trajectories and corresonding targets
        :param trajectories: list of trajectories
        :param targets: list of targets
        :param sample_share: share of sample size
        :return: list sampled trajectories and targets
        """
        sample_size = int(len(targets) * sample_share)

        sample_idx = range(len(targets))
        sample_idx = random.sample(sample_idx, sample_size)

        sample_trajs = [trajectories[i] for i in sample_idx]
        sample_targets = [targets[i] for i in sample_idx]

        return sample_trajs, sample_targets
        
    def fit(self, trajectories, targets, n_estimators, max_radius, min_trajectories, sample_share=0.66, processes=1):
        """
        Fit random forest
        :param trajectories: list of trajectories
        :param targets: list of targets
        :param n_estimators: the size of the forest
        :param max_radius: maximum radius in searching for decision point in trees
        :param min_trajectories: minimum number of trajectories to split further in trees
        :param sample_share: share of sample size
        :return: the builded forest
        """
        forest = Forest()
        
        if processes == 1:
            #serial option
            trees = [self.tree_fit(trajectories, targets, max_radius, min_trajectories, sample_share) for i in range(n_estimators)]

        else:
            #several processess option
            pool = mp.Pool(processes=processes)
            results = [pool.apply_async(self.tree_fit, args=(trajectories, targets, max_radius, min_trajectories, sample_share)) for i in range(n_estimators)]
            trees = [p.get() for p in results]
        
        #add trees to the forest
        for tree in trees:
            forest.add(tree)
            
        return forest

    def tree_fit(self, trajectories, targets, max_radius, min_trajectories, sample_share):
        """
        Get and fit single tree for the forest
        :param forest: fores to be fit
        :param trajectories: list of trajectories
        :param targets: list of targets
        :param max_radius: maximum radius in searching for decision point in trees
        :param min_trajectories: minimum number of trajectories to split further in trees
        :param sample_share: share of sample size
        :return: the builded forest
        """
        X_train, y_train = self.sample_traj(trajectories, targets, sample_share)

        clf = TreeBuilding()
        tree = clf.fit(X_train, y_train, max_radius, min_trajectories)

        return tree

            
        