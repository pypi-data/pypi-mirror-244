import pandas as pd
import numpy as np
from importlib import resources
from typing import Optional, Union
from scipy.stats import chi2_contingency, spearmanr, kendalltau, contingency
from sklearn.feature_selection import mutual_info_classif


class Features:
    """
    Feature selection methods for factors.
    """
    # TODO create feature selection class and add filter and other methods
