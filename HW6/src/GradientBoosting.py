import numpy as np 
from sklearn.base import BaseEstimator
from sklearn.tree import DecisionTreeRegressor
from sklearn.exceptions import NotFittedError


class GradientBoosting(BaseEstimator):
    """Gradient Boosting regressor class

    :method fit: fitting model
    """

    def __init__(
        self,
        n_estimator,
        pseudo_residual_func,
        learning_rate: float=0.1,
        min_sample: int=5,
        max_depth: int=3,
    ):
        """Initialize gradient boosting class
        
        :param n_estimator: number of estimators (i.e. number of rounds of gradient boosting)
        :pseudo_residual_func: function used for computing pseudo-residual
        :param learning_rate: step size of gradient descent
        :param min_sample: minimum number of samples in a leaf
        :param max_depth: maximum depth of the tree
        """
        self.n_estimator = n_estimator
        self.pseudo_residual_func = pseudo_residual_func
        self.learning_rate = learning_rate
        self.min_sample = min_sample
        self.max_depth = max_depth
        self._additive_models = []


    def fit(self, X, y):
        """Fit gradient boosting model

        :param train_data:
        :param train_target:
        """
        base_model = BaseLearner().fit(X, y)
        self._additive_models = [base_model]

        for i in range(self.n_estimator):
            curr_model = self._additive_models[i]
            neg_grads = self.pseudo_residual_func(y, curr_model.predict(X))
            next_model = DecisionTreeRegressor(min_samples_leaf=self.min_sample, max_depth=self.max_depth)
            # how to do curr_model + learning_rate * next_model??
            self._additive_models.append(next_model.fit(X, neg_grads))
        
        return self


    def predict(self, X):
        """Predict value

        :param X:
        """
        if not hasattr(self, "_additive_models"):
            raise NotFittedError(f"This {self.__class__.__name__} instance is not fitted yet. "
                "Call 'fit' with appropriate arguments before using this method.")
        n_rows, _ = X.shape
        preds = np.zeros(n_rows)
        for model in enumerate(self._additive_models):
            preds += self.learning_rate * model.predict(X)
        return preds


class BaseLearner(BaseEstimator):
    def __init__(self):
        pass

    def fit(self, X, y):
        """
        :param X: design matrix
        :param y: label examples
        :return: self
        """
        self._mean_y = np.mean(y)
        return self

    def predict(self, X):
        """Predict the mean

        :param X: 2d numpy array of training data
        :return: 
        """
        if not hasattr(self, "_mean_y"):
            raise NotFittedError(f"This {self.__class__.__name__} instance is not fitted yet. "
                "Call 'fit' with appropriate arguments before using this method.")

        n, _ = X.shape
        return self._mean_y * np.ones(n)

