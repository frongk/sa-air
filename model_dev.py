import pandas
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor

import shap
import pickle

DATA_FILE = 'data/model_data_w_energy_traffic.csv'
DATE_FILTER = ['20170201', '20180131']

FEATURE_FIELDS = ['Elevation', 
                  'Wind Speed - Scalar',
                  'Outdoor Temperature',
                  'a.lp_value',
                  'Volume',
                  'Occupancy',
                  'Speed',
                  'Weekday',
                  'Month',
                  'Time']

TARGET_FIELD = 'PM2.5'
MODEL_FILE = 'model/xgboost_PM2.5.pkl'

# feature functions
def get_month(date_value):
    month_str = str(date_value)[4:6]
    return int(month_str)

raw_data = pandas.read_csv(DATA_FILE)
data = raw_data.query(f'Date >=  {DATE_FILTER[0]} and \
                            Date <=  {DATE_FILTER[1]}')
data = data.assign(Month=raw_data['Date'].apply(get_month))

X = data[FEATURE_FIELDS]
X = X.fillna(-1)
y = data[TARGET_FIELD]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

parms = {
         'max_depth':[12,13,14], 
         'gamma' : [0.1,0.3, 0.5],
         'min_child_weight':[3,5,7]
        }

xgb = XGBRegressor(n_estimators=150, verbose=2)
cv_search =GridSearchCV(xgb, parms, cv=3, n_jobs=3, verbose=2)
cv_search.fit(X_train, y_train)
print(f'xgboost score: {cv_search.score(X_test,y_test)}')
print(f'xgboost parms:\n{str(cv_search.best_params_)}')
print(f'xgboost parms:\n{str(cv_search.best_estimator_.feature_importances_)}')

model = cv_search.best_estimator_
model_input_vars = FEATURE_FIELDS
pickle.dump([model, model_input_vars], open(MODEL_FILE, 'wb'))

# mlp = MLPRegressor(hidden_layer_sizes=(100,20,),verbose=True)
# mlp.fit(X_train, y_train)
# print(f'neural net score: {mlp.score(X_test,y_test)}')
