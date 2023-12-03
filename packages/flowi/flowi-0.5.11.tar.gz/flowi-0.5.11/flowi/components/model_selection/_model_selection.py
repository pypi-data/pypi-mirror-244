from typing import Any

import dask.dataframe as dd
import numpy as np
from scikeras.wrappers import KerasClassifier

from flowi.components.metrics._classification import Classification
from flowi.components.metrics._regression import Regression
from flowi.components.component_base import ComponentBase
from flowi.components.data_preparation import DataPreparationSKLearn
from flowi.components.models._wrappers import OneHotModel
from flowi.experiment_tracking.experiment_tracking import ExperimentTracking
from flowi.global_state import GlobalState
from flowi.utilities.logger import Logger
import hyperopt
from hyperopt import fmin, tpe, Trials


class ModelSelection(ComponentBase):
    def __init__(self):
        self._logger = Logger(logger_name=__name__)
        self._global_state = GlobalState()

    def _set_output(self, method_name: str, result: Any, methods_kwargs: dict) -> dict:
        experiment_tracking = ExperimentTracking()
        model = result[0]
        parameters = result[1]

        experiment_tracking.save_model(obj=model, file_path="model")
        experiment_tracking.log_model_param(key=model.__class__.__name__, value=parameters)
        return {
            "model": model,
            "parameters": parameters,
            "target_column": methods_kwargs["target_column"],
            "object": model,
        }

    def _score(self, y_pred, y_true) -> float:
        metric = self._global_state.get(key="metric")
        if metric == "accuracy":
            return Classification().accuracy(y_pred=y_pred, y_true=y_true)
        elif metric == "precision":
            return Classification().precision(y_pred=y_pred, y_true=y_true, average="micro")
        elif metric == "recall":
            return Classification().recall(y_pred=y_pred, y_true=y_true, average='micro')
        elif metric == "f1_score":
            return Classification().f1_score(y_pred=y_pred, y_true=y_true, average='micro')
        elif metric == "mean_squared_error":
            return Regression().mean_squared_error(y_pred=y_pred, y_true=y_true)
        elif metric == "mean_absolute_error":
            return Regression().mean_absolute_error(y_pred=y_pred, y_true=y_true)
        elif metric == "mean_squared_log_error":
            return Regression().mean_squared_log_error(y_pred=y_pred, y_true=y_true)
        elif metric == "r2_score":
            return Regression().r2_score(y_pred=y_pred, y_true=y_true)

        raise ValueError(f"Metric '{metric}' not implemented")

    def tpe(
        self,
        df: dd.DataFrame,
        target_column: str,
        model,
        parameters: dict,
        early_stopping: bool or str = None,
        n_trials: int = 10,
        cv: int = 5,
    ):
        if isinstance(model, OneHotModel):
            flowi_model = model
            model = flowi_model.model

            sklean_data_prep = DataPreparationSKLearn()
            X, y = sklean_data_prep.prepare_train(df=df, target_column=target_column)
            y = flowi_model.encode(y)
        else:
            flowi_model = model
            model = flowi_model.model

            sklean_data_prep = DataPreparationSKLearn()
            X, y = sklean_data_prep.prepare_train(df=df, target_column=target_column)
            y = flowi_model.encode(y)

        X = X.compute()
        y = y.compute()

        best_model = None
        best_score = np.Inf
        best_params = dict()

        def objective(params):
            nonlocal best_params, best_score, best_model

            initial_params = model.get_params()
            new_params = initial_params | params
            klass = model.__class__
            new_object = klass(**new_params)
            new_object.fit(X, y)

            y_pred = new_object.predict(X)
            score = self._score(y_true=y, y_pred=y_pred)

            if score < best_score:
                best_score = score
                best_model = new_object
                best_params = new_params

            return {
                'loss': score,
                'status': hyperopt.STATUS_OK,
                'model': new_object
            }

        trials = Trials()
        fmin(fn=objective,
             space=parameters,
             algo=tpe.suggest,
             max_evals=n_trials,
             trials=trials,
        )

        model = best_model
        self._logger.debug(f"Model: {model.__class__.__name__}")
        self._logger.debug(f"Best Parameters: {best_params}")

        if isinstance(model, KerasClassifier):
            flowi_model.model = model
            model = flowi_model
        else:
            flowi_model.model = model
            model = flowi_model

        return model, best_params
