import pickle
import numpy as np
import pandas as pd
from scindo_input_ingestion import Scindo_ingestion


class Default_estimator:

    def __init__(self):

        # make ingestion object
        self.ingest = Scindo_ingestion()

        # read model of prior
        self.prior_model = pickle.load(open('built_models/prior_p_regressor.pkl', 'rb'))

        # read ml model: Complement NB
        self.cnb = pickle.load(open('built_models/model_cnb.sav', 'rb'))

        # read ml model: SVC
        self.svc = pickle.load(open('built_models/model_svc.sav', 'rb'))

        # read ml model: Logistic Regression
        self.lr = pickle.load(open('built_models/model_lr.sav', 'rb'))

        # read the Encoder
        self.encoder = pickle.load(open("built_models/encoder.sav", 'rb'))

    def build_beta_binomial_distribution(self, sample_mean:float, sample_power:int) -> list:
        alpha = sample_power * sample_mean
        beta = sample_power - alpha
        return [alpha, beta]

    def prior_calculator(self, data:dict) -> float:
        age = data["age_id"]
        gender = data["gender_id"]
        location = data["region_id"]
        profession = data["profession_id"]
        education = data["education_id"]

        # prior:
        X = pd.DataFrame( [(age, gender, location, education, profession)],
            columns=["age_id", "gender_id", "region_id", "education_id", "profession_id"])
        prior = self.prior_model.predict(X)

        max_prior = 0.062
        prior = prior[0] / max_prior

        print("Prior: ", prior)
        return prior

    def score_calculator(self, data:dict) -> float:

        # anagraphical data
        job = data["job_presence"]
        profession = data["profession_id"]
        
        # transactional data
        outflow = data["outflow"]
        avg_balance = data["avg_balance"]
        salary_on_acc = data["salary_on_acc"]
        active_rids = data["active_rids"]
        deposits = data["deposits"]
        investments = data["investments"]
        other_loans = data["other_loans"]
        other_mortgages = data["other_mortgages"]

        # scindo db
        scindo_number_of_loans = data["completed_loans"]
        scindo_default = data["scindo_default"]
        

        weight = {
            "employment" : 0.25,
            "job_position" : 0.15,
            "completed_loans" : 0.15,
            "salary_on" : 0.25,
            "active_rids" : 0.15,
            "avg_balance" : 0.15,
            "outflow" : 0.15,
            "out/avg" : 0.15,
            "investments" : 0.15,
            "other_loans" : 0.15,
            "other_mortgages" : 0.15,
            "deposits" : 0.15
        }
        sign = {
            "employment" : 1 if job in [True, 1] else 0,
            "job_position" : 1 if not profession in [1, 2, 5, 7] else 0,
            "completed_loans" : 1 if scindo_number_of_loans >= 1 else 0,
            "salary_on" : 1 if salary_on_acc == 1 else 0,
            "active_rids" : 1 if active_rids >= 5 else 0,
            "avg_balance" : 1 if avg_balance >= 1000 else 0,
            "outflow" : 1 if (outflow >= 1000) & (outflow <= 5000)else 0,
            "out/avg" : 1 if outflow/(avg_balance+100) <= 30 else 0,
            "investments" : 1 if investments >= 1000 else 0,
            "other_loans" : 1 if (other_loans <= 10000) & (other_loans >= 1000) else 0,
            "other_mortgages" : 1 if (other_mortgages <= 100000) & (other_mortgages >= 1000) else 0,
            "deposits" : 1 if deposits >= 1000 else 0
        }

        # calculate on main domain then scale

        # main domain
        min_score = 0
        max_score = 2

        credit_score = 0

        # calculate credit score
        for k, v in sign.items(): credit_score += sign[k] * weight[k]
        for k, v in sign.items():  sign[k] = 0

        # scale the score to [0, 1.6] domain
        credit_score = credit_score + np.abs(min_score)

        # calculate the credit score
        if scindo_default == 1: credit_score = 0

        # calculate score in [0,1] domain
        credit_score = credit_score / max_score
        if credit_score <= 0: credit_score = 0

        # default probability calculation
        c1 = 0.0095
        c2 = 0.05
        c3 = 0.005
        x = credit_score

        probability_of_default = c1  * ((1 - x)/(c2 + x)) # - c3

        max_score = 0.2
        probability_of_default = probability_of_default / max_score
        print("Scorecard: ", probability_of_default)
        return probability_of_default

    def ml_calculator(self, data:dict) -> float:

        df = pd.DataFrame(data, index=[0])
        
        X = df.loc[:, df.columns]
        X_encoded = self.encoder.transform(X)

        # predict and aggregate the result
        cnb_f1 = 0.66
        svc_f1 = 0.55
        lr_f1 = 0.73
        sum = cnb_f1 + svc_f1 + lr_f1

        cnb_prediction = self.cnb.predict(X_encoded) * cnb_f1
        svc_prediction = self.svc.predict(X_encoded) * svc_f1
        lr_prediction = self.lr.predict(X_encoded) * lr_f1

        result = (cnb_prediction + svc_prediction + lr_prediction) / 3

        print("ML: ", result[0])
        return round(result[0], 2)

    def run(self, data:dict) -> float:
        
        # render the body to flat format
        data = self.ingest.body_flatener(data)

        # prior
        p1 = self.prior_calculator(self.ingest.prior_body_builder(data))
        beta1 = self.build_beta_binomial_distribution(p1, 10)

        print("beta-prior: ", beta1)
        # score
        p2 = self.score_calculator(self.ingest.scorecard_body_builder(data))
        beta2 = self.build_beta_binomial_distribution(p2, 85)
        print("beta-score: ", beta2)

        # ml
        p3 = self.ml_calculator(self.ingest.ml_body_builder(data))
        beta3 = self.build_beta_binomial_distribution(p3, 5)
        print("beta-ml: ", beta3)

        # mix them up
        alpha = beta1[0] + beta2[0] + beta3[0]
        beta = beta1[1] + beta2[1] + beta3[1]
        peak_of_distribution = alpha / (alpha + beta)

        # threshould : 0.0475 on Pd
        threshould = 0.0475
        probability_of_default = peak_of_distribution

        if  probability_of_default >= threshould:
            default = 1
        else:
            default = 0
        
        if probability_of_default <= 0: probability_of_default = 0

        return { "UserID": data["UserID"], "default_probability" : round(probability_of_default, 4), "sign" : default}
        



        
