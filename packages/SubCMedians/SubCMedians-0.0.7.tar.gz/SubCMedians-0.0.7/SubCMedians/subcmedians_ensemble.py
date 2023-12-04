import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
from tqdm.autonotebook import tqdm
from collections import Counter
from SubCMedians.subcmedians import subcmedians

class subcmedians_ensemble:
    def __init__(self, D, nb_estimators, Gmax=300, H=200, nb_iter=10000,random_state=None):
        """SubCMedians subspace clustering.

        Parameters
        ----------
        D : int
            Dataset full dimensionality
        nb_estimators : int
            Number of estimators
        Gmax : int, default=300
            Maximal model size, i.e., maximal number of coordinates that can
            be included in the model
        H : int, default=200
            Size of the sliding window used for training
        nb_iter : int, default=10000
            Number of iterations of the SubCMedians algorithm
        random_state : int, RandomState instance, default=None
            Determines random number generation for centroid initialization. Use
            an int to make the randomness deterministic.
            See :term:`Glossary <random_state>`.

        Attributes
        ----------
        subcmedians_models : list 
            List of subcmedians objects
        cluster_centers_ : ndarray of shape (n_clusters, n_features)
            Coordinates of cluster centers.
        subspaces_  : ndarray of shape (n_clusters, n_features)
            Subspace of cluster centers.
        labels_ : ndarray of shape (n_samples,)
            Labels of each point
        sae_ : float
            Sum of Absolute Errors between data instances and their closest center

        Examples
        --------
        >>> from SubCMedians.subcmedians import subcmedians
        >>> from SubCMedians.data_generator import make_subspace_blobs
        >>> D = 20
        >>> dataset_params={"p_dim": 0.7,
                            "n_samples":5000,
                            "n_features":D,
                            "centers":12}
        >>> X,y_true,ss = make_subspace_blobs(**dataset_params)
        >>> X = (X - X.mean(axis=0))/ X.std(axis=0)
        >>> nb_estimators = 10
        >>> scm = subcmedians_ensemble(D, nb_estimators, Gmax=300, H=200, nb_iter=10000)
        >>> scm.fit(X)
        >>> scm.predict(X)
        """
        self.subcmedians_models = []
        for i in range(nb_estimators):
            if random_state is not None:
                local_random_state = random_state+i
            else:
                local_random_state = None
            self.subcmedians_models.append(subcmedians(D, Gmax=Gmax, H=H, nb_iter=nb_iter, random_state=local_random_state))
        self.Gmax = Gmax
        self.H = H
        self.D = D
        self.nb_iter = nb_iter
        self.S = {}
        self.random_state = random_state
        self.cluster_centers_ = None

    def get_all_cluster_centers(self):
        '''
        Get all the models cluster centers in a single data frame

        Returns
        -------
        pandas.DataFrame
            cluster centers locations
        '''
        self.cluster_centers_ = [m.cluster_centers_.copy() for m in self.subcmedians_models]
        for i,m in enumerate(self.cluster_centers_):
            self.cluster_centers_[i].index = [str(i)+"-"+str(v) for v in self.cluster_centers_[i].index]
        self.cluster_centers_ = pd.concat(self.cluster_centers_)
        return self.cluster_centers_

    def predict(self, X):
        """
        Compute the cluster membership of the data instance from $X$

        Parameters
        ----------
        X : numpy.array
            Data set to be clustered, rows represent instances (points) and
            columns represent features (dimensions)

        Returns
        -------
        numpy.array
            cluster memberships

        """
        if self.cluster_centers_ is None:
            self.get_all_cluster_centers()
        X = np.asarray(X)
        if len(X.shape) == 1:
            X = X.reshape(1,-1)

        distances = pairwise_distances(X,
                                       self.cluster_centers_,
                                       metric="l1",
                                       n_jobs=None)
        self.labels_ = np.argmin(distances,axis=1)
        self.sae_ = distances[range(distances.shape[0]),self.labels_]
        return(self.cluster_centers_.index[self.labels_])


    def sae_score(self, X):
        """
        Compute the Sum of Absolute Errors (SAE) of dataset $X$ with respect to
        the current clustering model, a low SAE means a better quality

        Parameters
        ----------
        X : numpy.array
            Data set to be clustered, rows represent instances (points) and
            columns represent features (dimensions)

        Returns
        -------
        float
            Sum of Absolute Errors

        """
        if self.cluster_centers_ is None:
            self.get_all_cluster_centers()
        X = np.asarray(X)
        if len(X.shape) == 1:
            X = X.reshape(1,-1)

        distances = pairwise_distances(X,
                                       self.cluster_centers_,
                                       metric="l1",
                                       n_jobs=None)
        sae = distances.min(axis=1).sum()
        return(sae)


    def fit(self, X, lazy=False, collector=False):
        """
        Build the SubCMedians model associated to dataset $X$

        Parameters
        ----------
        X : numpy.ndarray
            Data set to be clustered, rows represent instances (points) and
            columns represent features (dimensions)
        lazy: bool, default=False
            If true only tries to update the model iif the SAE increased when
            the datasample was updated, otherwise the optimization iteration is
            permormed at each sample update
        collector: bool, default=False
            If true all the models, and conserved modifications are kept.

        Returns
        -------
        subcmedians_ensemble
            Fitted subcmedians instance

        """
        for m in self.subcmedians_models:
            m.fit(X, lazy, collector)
        return(self)


    def fusion(self, X, top_centers, Gmax=300, H=200, nb_iter=10000, random_state=None):
        """
        Make a fusion of the best centers from an ensemble of subcmedian models into a single subcmedian
        model and fits the model.

        Parameters
        ----------
        X : numpy.array
            Data set to be clustered, rows represent instances (points) and
            columns represent features (dimensions)
        top_centers : int
            Number of top centers from the ensemble of subcmedians to be kept in the fusion model
        Gmax : int, default=300
            Maximal model size, i.e., maximal number of coordinates that can
            be included in the model
        H : int, default=200
            Size of the sliding window used for training
        nb_iter : int, default=10000
            Number of iterations of the SubCMedians algorithm
        random_state : int, RandomState instance, default=None
            Determines random number generation for centroid initialization. Use
            an int to make the randomness deterministic.
            See :term:`Glossary <random_state>`.

        Returns
        -------
        float
            Sum of Absolute Errors for the fusion model

        """
        self.fusion_individual = subcmedians(self.D, Gmax, H, nb_iter, random_state)
        y_pred = self.predict(X)
        most_common = Counter(y_pred).most_common(top_centers)
        i = 0
        for c,nb_points in most_common:
            for d in range(self.D):
                x = self.cluster_centers_.loc[c,d]
                if x:
                    self.fusion_individual.model._candidate_insertion = (i,d,x)
                    self.fusion_individual.model.try_insertion()
                    self.fusion_individual.model.apply_changes()
            i += 1
        return self.fusion_individual.fit(X)


    def predict_many_coocurrence(self,X):
        Y = np.stack([m.predict(X) for m in self.subcmedians_models])
        coocurence = np.zeros((Y.shape[1],Y.shape[1]))
        for i in range(Y.shape[1]):
            for j in range(i+1, Y.shape[1]-1):
                n = sum(Y[:,i] == Y[:,j])
                coocurence[i,j] = n
                coocurence[j,i] = n
        return coocurence

