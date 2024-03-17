import pandas as pd
import numpy as np
from sklearn.metrics import balanced_accuracy_score, average_precision_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import ComplementNB
from sklearn.svm import SVC
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

class Ml_builder:

    def __init__(self, df:pd.DataFrame) -> None:
        df.set_index("id", inplace=True)
        print(df.columns)
        self.df = df
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        self.X = df.loc[:, df.columns != "sign"]
        self.y = df["sign"]
        self.encoder.fit(self.X)


    def metrics_calculator(self, y_true:pd.Series, y_pred:pd.Series) -> dict:

        metrics = {
            "precision" : np.round(average_precision_score(y_true, y_pred), 2),
            "f1_score" : np.round(f1_score(y_true, y_pred), 2),
            "bacc" : np.round(balanced_accuracy_score(y_true, y_pred), 2)
        }

        return metrics
    
    def ml_logistic_regression(self):
        
        X = self.encoder.transform(self.X)
        y = self.y

        cumsum_f1 = 0

        strat_kfold = StratifiedKFold(n_splits=3, random_state=42, shuffle=True)
        # l1 : manhatan distance : pesi a zero, molto robusto per outliers
        # l2 : somma dei quadrati dei pesi : molti bassi ma non zero
        model = LogisticRegression(class_weight='balanced', solver="saga", penalty="l2")

        # enumerate the splits
        for train_ix, test_ix in strat_kfold.split(X, y.values):
            
            # select rows
            X_train = X[train_ix, :]
            X_test = X[test_ix, :]
            y_train = y.loc[train_ix]
            y_test = y.loc[test_ix]
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            metrics = self.metrics_calculator(y_test, y_pred)
            cumsum_f1 += metrics["f1_score"]
        
        mean_f1 = np.round(cumsum_f1 / 3, 2)

        return (model, mean_f1)

    def ml_complement_nb(self) -> tuple:
         
        X = self.encoder.transform(self.X)
        y = self.y

        cumsum_f1 = 0

        strat_kfold = StratifiedKFold(n_splits=3, random_state=42, shuffle=True)
        model = ComplementNB(fit_prior=True)

        # enumerate the splits
        for train_ix, test_ix in strat_kfold.split(X, y.values):
            
            # select rows
            X_train = X[train_ix, :]
            X_test = X[test_ix, :]
            y_train = y.loc[train_ix]
            y_test = y.loc[test_ix]
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            metrics = self.metrics_calculator(y_test, y_pred)
            cumsum_f1 += metrics["f1_score"]
        
        mean_f1 = np.round(cumsum_f1 / 3, 2)

        return (model, mean_f1)

    def ml_svc(self) -> tuple:

        model = SVC(class_weight='balanced', probability=True, random_state=42)
        strat_kfold = StratifiedKFold(n_splits=3, random_state=42, shuffle=True)

        cumsum_f1 = 0

        # enumerate the splits
        X = self.encoder.transform(self.X)
        y = self.y
        

        for train_ix, test_ix in strat_kfold.split(X, y.values):
            
            # select rows
            X_train = X[train_ix, :]
            X_test = X[test_ix, :]
            y_train = y.loc[train_ix]
            y_test = y.loc[test_ix]
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            metrics = self.metrics_calculator(y_test, y_pred)
            cumsum_f1 += metrics["f1_score"]
        
        mean_f1 = np.round(cumsum_f1 / 3, 2)

        return (model, mean_f1)

    def label_preparer(self, df:pd.DataFrame) -> pd.DataFrame:
        
        # For outlier detectors such as isolation forest and one class svm
        # there is the need to modify the [0:good payer, 1:bad payer] to [-1, 1] respectively

        for idx, row in df.iterrows():
            
            # bad payer
            if row["sign"] == 1:
                df.loc[idx, "sign"] = 1
            
            # good payer
            elif row["sign"] == 0:
                df.loc[idx, "sign"] = -1

        return df

    def pollution_cleaner(self, df:pd.DataFrame) -> pd.DataFrame:
       
       df_clean = df[df["sign"] == +1]
       df_pollution = df[df["sign"] == -1]
       
       return df_clean, df_pollution

    def ml_isolation_forest(self) -> tuple:
        
        # instantiate the model
        model = IsolationForest(contamination=0.01, max_features=6, random_state=1)

        # prepare the label for outlier detector
        df = self.label_preparer(self.df)

        # split the data to train and test
        df_train, df_test = train_test_split(df, test_size=0.3, random_state=42)

        # clean train data, encode, and fit the model
        df_train_clean, df_train_pollution = self.pollution_cleaner(df_train)
        X_train = df_train_clean.loc[:, df_train_clean.columns != "sign"]
        X_encoded = self.encoder.transform(X_train)
        model.fit(X_encoded)

        # make the test set and predict
        df_test = pd.concat([df_test, df_train_pollution])
        X_test = df_test.loc[:, df.columns != "sign"]
        y_test = df_test.loc[:, "sign"]
        X_encoded = self.encoder.transform(X_test)
        y_pred = model.predict(X_encoded)

        # test the model
        model_details = self.metrics_calculator(y_test, y_pred)
        f1 = model_details["f1_score"]
        
        return (model, f1)
    
    def ml_oneclass_svm(self) -> tuple:
        
        # instantiate the model
        model = OneClassSVM(kernel="rbf", nu=0.01, gamma="auto")

        # prepare the label for outlier detector
        df = self.label_preparer(self.df)

        # split the data to train and test
        df_train, df_test = train_test_split(df, test_size=0.3, random_state=42)

        # clean train data and fit the model
        df_train_clean, df_train_pollution = self.pollution_cleaner(df_train)
        X_train = df_train_clean.loc[:, df_train_clean.columns != "sign"]
        X_encoded = self.encoder.transform(X_train)
        model.fit(X_encoded)

        # make the test set and predict
        df_test = pd.concat([df_test, df_train_pollution])
        X_test = df_test.loc[:, df.columns != "sign"]
        y_test = df_test.loc[:, "sign"]
        X_encoded = self.encoder.transform(X_test)
        y_pred = model.predict(X_encoded)

        # test the model
        model_details = self.metrics_calculator(y_test, y_pred)
        f1 = model_details["f1_score"]
        
        return (model, f1)
