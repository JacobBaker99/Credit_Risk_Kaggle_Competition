#!/usr/bin/env python3

'''Neural Network for Project One

This module is used to conduct neural networks on train_person1.csv, train_person2.csv,
and train_base.csv. This is the neural network with 150 hidden layers.
'''

import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn import neural_network
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer

# pylint: disable=C0103

__author__ = 'Frontline'
__version__ = 'Spring 2024'
__pylint__ = '2.14.5'

SEED = 3270

def fit():
    """
    Fit the data to the model.
    """
     # We need to turn data strings into numbers that Sklearn can process, onehotencoding
    one_hot = OneHotEncoder()
    trans = ColumnTransformer([("one_hot", one_hot, cat_features)], remainder="passthrough")
    encoded_features = trans.fit_transform(features).toarray()
    one_hot_features = trans.named_transformers_['one_hot'].get_feature_names_out(cat_features)
    remaining_features = [f for f in features.columns if f not in cat_features]
    all_feature_names = list(one_hot_features) + remaining_features
    assert len(all_feature_names) == encoded_features.shape[1], "Mismatch in feature count"

    X = pd.DataFrame(encoded_features, columns=all_feature_names)
    y = labels
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)  # X is your dat
    return X_scaled, y

def test(X_scaled, y):
    """
    Testing the folds of the fitted data. And a test of the overall accuracy.
    """
    HIDDEN_LAYERS = (150)
    SOLVER = 'adam'
    MAX_ITER = 1000
    ACTIVATION = 'logistic'

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    for train_index, test_index in skf.split(X_scaled, y):
        X_train, X_test = X_scaled[train_index], X_scaled[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        mlp_model = neural_network.MLPClassifier(solver=SOLVER, hidden_layer_sizes=HIDDEN_LAYERS,
            max_iter=MAX_ITER, activation=ACTIVATION, random_state=SEED)
        mlp_model.fit(X_train, y_train)
        print(f'\tMLP: {accuracy_score(y_test, mlp_model.predict(X_test)) * 100:.2f}%')

    mlp_scores = cross_val_score(neural_network.MLPClassifier(solver=SOLVER,
        hidden_layer_sizes=HIDDEN_LAYERS, max_iter=MAX_ITER, activation=ACTIVATION,
        random_state=SEED), X_scaled, y, cv=skf, scoring="accuracy")
    print(f'MLP Scores: {mlp_scores.mean():.2f} ± {mlp_scores.std():.2f}')

if __name__ == '__main__':
    data = pd.read_csv(r'dev.csv')
    data.drop("case_id", axis=1, inplace=True)
    data = data.astype(str)

    for column in data.columns:
        if data[column].dtype == 'object':  # Checking for string/object type
            data[column].fillna("0", inplace=True)

    feature_list = [
    "birth_259D","contaddr_smempladdr_334L","empl_employedtotal_800L",
        "empl_industry_691L","familystate_447L","housetype_905L",
        "incometype_1044T","mainoccupationinc_384A","num_group1",
        "personindex_1023L","persontype_1072L","persontype_792L",
        "role_1084L","safeguarantyflag_411L","sex_738L","type_25L"
    ]
    features = data[feature_list]
    labels = data['target']

    cat_features = [
    "birth_259D","contaddr_smempladdr_334L","empl_employedtotal_800L",
    "empl_industry_691L","familystate_447L","housetype_905L",
    "incometype_1044T","mainoccupationinc_384A","num_group1",
    "personindex_1023L","persontype_1072L","persontype_792L",
    "role_1084L","safeguarantyflag_411L","sex_738L","type_25L"
    ]

    X_scale, Y = fit()
    test(X_scale, Y)
