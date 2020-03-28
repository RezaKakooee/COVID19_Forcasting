# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 02:11:04 2020

@author: rkako
"""

"""# ML analysis"""

y_train = confirmed_group.iloc[0,1:int(num_days*0.85)].values
y_valid = confirmed_group.iloc[0, int(num_days*0.85):].values

num_train_days = len(y_train)
num_valid_days = len(y_valid)

x_train = np.arange(0, num_train_days).reshape(-1, 1)
x_valid = np.arange(0, num_valid_days).reshape(-1, 1)

from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
from fbprophet import Prophet
from sklearn.preprocessing import PolynomialFeatures

param_grid = {'kernel':['linear', 'rbf','poly'],
            'C':[0.01, 0.1, 1, 10],
            'gamma':[0.01, 0.1, 1],
            'shrinking':[True, False]}

svm = SVR(degree=3)

svm_search = RandomizedSearchCV(svm, param_grid, cv=5, return_train_score=True)

svm_search.fit(X=x_train, y=np.ravel(y_train))

svm_search.best_estimator_

prediction_valid_svm = svm_search.best_estimator_.predict(x_valid)

print('prediction_valid_svm:\n', prediction_valid_svm)

print("Root Mean Square Value:", np.sqrt(mean_squared_error(y_valid,prediction_valid_svm)))

"""# XGBoost"""

import xgboost as xgb
import hyperopt
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials

space={'max_depth': hp.quniform("max_depth", 3, 18, 1),
        'gamma': hp.uniform ('gamma', 1,9),
        'reg_alpha' : hp.quniform('reg_alpha', 40,180,1),
        'reg_lambda' : hp.uniform('reg_lambda', 0,1),
        'colsample_bytree' : hp.uniform('colsample_bytree', 0.5,1),
        'min_child_weight' : hp.quniform('min_child_weight', 0, 10, 1),
        'n_estimators': 180
    }

#Regression: 
def hyperparameter_tuning(space):
    reg=xgb.XGBRegressor(objective ='reg:squarederror',
                         n_estimators=1000,
                         max_depth = int(space['max_depth']), 
                         gamma = space['gamma'],
                         reg_alpha = int(space['reg_alpha']),
                         min_child_weight=space['min_child_weight'],
                         colsample_bytree=space['colsample_bytree'])
    
    evaluation = [( x_train, y_train), ( x_valid, y_valid)]
    
    reg.fit(x_train, y_train,
            eval_set=evaluation, eval_metric="rmse",
            early_stopping_rounds=10,verbose=False)

    pred = reg.predict(x_valid)
    mse= mean_squared_error(y_valid, pred)
    # print ("SCORE:", mse)
    #change the metric if you like
    return {'loss':mse, 'status': STATUS_OK }

trials = Trials()
best = fmin(fn=hyperparameter_tuning,
            space=space,
            algo=tpe.suggest,
            max_evals=100,
            trials=trials)

print (best)

best

xg_reg = xgb.XGBRegressor(objective ='reg:squarederror', 
                          colsample_bytree = best['colsample_bytree'], 
                          gamma = best['gamma'],
                          learning_rate = 0.1,
                          min_child_weigh=best['min_child_weight'],
                          max_depth = int(best['max_depth']), 
                          reg_alpha = best['reg_alpha'],
                          reg_lambda = best['reg_lambda'],
                          alpha = 10, 
                          n_estimators = 1000)

xg_reg.fit(x_valid, y_valid)

xgb_preds = xg_reg.predict(x_valid)

print("Root Mean Square Value:", np.sqrt(mean_squared_error(y_valid, xgb_preds)))