from scindo_input_ingestion import Scindo_ingestion

class Input_controller:

    def __init__(self) -> None:
        
        self.ingest = Scindo_ingestion()

        self.all_variables = [
            "UserID", "User_GenericInfo_Birth", "User_GenericInfo_Address", "User_GenericInfo_Gender", "User_GenericInfo_Type",
            "User_Job_Employed", "User_Job_Sector", "User_Job_Position", "User_Job_Education",
            "User_Behaviour_RegistrationDatetime", "User_Behaviour_OnboardingTime",
            "User_Behaviour_Device", "User_Behaviour_Lifetime", "User_Behaviour_WeeklyVisitNumber", "User_Behaviour_Default",
            "User_Finance_TotalLoans_Number", "User_Finance_LoansAmount", "User_Finance_TotalLoans_Salary",
            "User_Finance_RID", "User_Finance_AvarageCreditSpending", "User_Finance_AvarageTransactionsAmount",
            "User_Finance_AvarageAccountSpending", "User_Finance_Cumsum_In", "User_Finance_Cumsum_Out",
            "User_Finance_Balance_Avg", "User_Finance_Balance_Min", "User_Finance_Balance_Max", "User_Finance_Balance_Withdrawls",
            "User_Finance_EoP_Deposit", "User_Finance_EoP_Investments", "User_Finance_EoP_Loans", "User_Finance_EoP_Mortgages"
        ]
    
    def keys_controller_tree(self, initial_body:dict) -> dict:
        
        # control vars
        flag, code, error = False, 200, ""

        # 1)
        variables_1st_layer = ["UserID", "User"]
        for variable in variables_1st_layer:
            
            if not variable in initial_body.keys():
                
                flag, code, error = True, 400, 'variable {} is missing in input, please send a valid request'.format(variable)
                
                return {"flag" : flag, "response" : error, "response_code" : code}
        
        # 2)
        variables_user_layer = ["Behaviour", "Finance", "GenericInfo", "Job"]
        for variable in variables_user_layer:

            if not variable in initial_body["User"].keys():

                flag, code, error = True, 400, 'variable User_{} is missing in input, please send a valid request'.format(variable)
                
                return {"flag" : flag, "response" : error, "response_code" : code}

        # 3)
        variables_behaviour_layer = ["Default", "Device", "Lifetime", "OnboardingTime", "RegistrationDatetime",
            "WeeklyVisitNumber"]
        for variable in variables_behaviour_layer:
            
            if not variable in initial_body["User"]["Behaviour"].keys():
                
                flag, code, error = True, 400, 'variable User_Behaviour_{} is missing in input, please send a valid request'.format(variable)
                
                return {"flag" : flag, "response" : error, "response_code" : code}
        
        # 4)
        variables_genericinfo_layer = ["Address", "Birth", "Gender", "Type"]
        for variable in variables_genericinfo_layer:
            
            if not variable in initial_body["User"]["GenericInfo"].keys():
                
                flag, code, error = True, 400, 'variable User_GenericInfo_{} is missing in input, please send a valid request'.format(variable)
   
                return {"flag" : flag, "response" : error, "response_code" : code}

        # 5)
        variables_job_layer = ["Education", "Employed", "Position", "Sector"]
        for variable in variables_job_layer:

            if not variable in initial_body["User"]["Job"].keys():

                flag, code, error = True, 400, 'variable User_Job_{} is missing in input, please send a valid request'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

        # 6)
        variables_finance_layer = ["AvarageAccountSpending", "AvarageCreditSpending", "AvarageTransactionsAmount", "RID",
            "Balance", "Cumsum", "EoP", "TotalLoans"]
        for variable in variables_finance_layer:

            if not variable in initial_body["User"]["Finance"].keys():

                flag, code, error = True, 400, 'variable User_Finance_{} is missing in input, please send a valid request'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

        # 7)
        variables_balance_layer = ["Avg", "Max", "Min", "Withdrawls"]
        for variable in variables_balance_layer:

            if not variable in initial_body["User"]["Finance"]["Balance"].keys():

                flag, code, error = True, 400, 'variable User_Finance_Balance_{} is missing in input, please send a valid request'.format(variable)
 
                return {"flag" : flag, "response" : error, "response_code" : code}

        # 8)
        variables_cumsum_layer = ["In", "Out"]
        for variable in variables_cumsum_layer:

            if not variable in initial_body["User"]["Finance"]["Cumsum"].keys():

                flag, code, error = True, 400, 'variable User_Finance_Cumsum_{} is missing in input, please send a valid request'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

        # 9)
        variables_eop_layer = ["Deposit", "Investments", "Loans", "Mortgages"]
        for variable in variables_eop_layer:

            if not variable in initial_body["User"]["Finance"]["EoP"].keys():

                flag, code, error = True, 400, 'variable User_Finance_EoP_{} is missing in input, please send a valid request'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

        # 10)
        variables_totalloans_layer = ["Amount", "Number", "Salary"]
        for variable in variables_totalloans_layer:

            if not variable in initial_body["User"]["Finance"]["TotalLoans"].keys():

                flag, code, error = True, 400, 'variable User_Finance_TotalLoans_{} is missing in input, please send a valid request'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

        return {"flag" : flag, "response" : error, "response_code" : code}

    def keys_controller_flat(self, body:dict):
        
        # check variable presence
        error, flag, code = '', '', False, 200
        for variable in self.all_variables:
            if not variable in body.keys():
                error = 'variable {} is missing in input, please send a valid request'.format(variable)
                flag, code = True, 400
                break

        return {"flag" : flag, "response" : error, "response_code" : code}

    def type_check_int(self, body:dict):
        
        # integer variables: 17
        self.int_variables = [
            "UserID", "User_GenericInfo_Address", "User_GenericInfo_Gender", "User_GenericInfo_Type", "User_Job_Sector",
            "User_Job_Position", "User_Job_Education", "User_Behaviour_Device",
            "User_GenericInfo_Birth",  "User_Behaviour_OnboardingTime",
            "User_Behaviour_Lifetime", "User_Behaviour_WeeklyVisitNumber", "User_Finance_TotalLoans_Number", 
            "User_Finance_RID", "User_Finance_AvarageCreditSpending",
            "User_Finance_AvarageAccountSpending", "User_Finance_Balance_Withdrawls"
            # "User_Behaviour_RegistrationDatetime",
            ]

        # check 
        flag, code, error = False, 200, ""
        for variable in self.int_variables:
            
            x = body[variable]
            if not type(x) in [int]:

                flag, code, error = True, 422, 'variable {} should be a positive integer number, please send a valid request'.format(variable)
                break

            elif x < 0 :
                
                flag, code, error = True, 422, 'variable {} should be a positive integer number, please send a valid request'.format(variable)
                break
        
        return {"flag" : flag, "response" : error, "response_code" : code}

    def type_check_float(self, body:dict):
        
        # float variables: 11
        self.float_variables = [
            "User_Finance_LoansAmount", "User_Finance_AvarageTransactionsAmount",
            "User_Finance_Cumsum_In", "User_Finance_Cumsum_Out",
            "User_Finance_Balance_Avg", "User_Finance_Balance_Min", "User_Finance_Balance_Max",
            "User_Finance_EoP_Deposit", "User_Finance_EoP_Investments", "User_Finance_EoP_Loans", "User_Finance_EoP_Mortgages"
            ]

        # check
        flag, code, error = False, 200, ""
        for variable in self.float_variables:
            
            x = body[variable]
            if not type(x) in [int, float]:

                flag, code, error = True, 422, 'variable {} should be a positive float number, please send a valid request'.format(variable)
                break

            elif x < 0 :
                
                flag, code, error = True, 422, 'variable {} should be a positive float number, please send a valid request'.format(variable)
                break

        return {"flag" : flag, "response" : error, "response_code" : code}
    
    def type_check_bool(self, body:dict):
        
        # bool variables: 3
        self.boolean_variables = [
            "User_Job_Employed", "User_Behaviour_Default", "User_Finance_TotalLoans_Salary"
            ]

        # check
        flag, code, error = False, 200, ""
        for variable in self.boolean_variables:
            x = body[variable]

            if not type(x) in [bool]:

                flag, code, error = True, 422, 'variable {} should be a boolean number, please send a valid request'.format(variable)

                break
        
        return {"flag" : flag, "response" : error, "response_code" : code}
        
    def value_check_encoded(self, body:dict):
        
        # encoded variables
        self.encoded_variables = {
            "User_GenericInfo_Address" : {"lower": 1, "upper": 20},
            "User_GenericInfo_Gender" : {"lower": 1, "upper": 3},
            "User_GenericInfo_Type" : {"lower": 1, "upper": 2},
            "User_Job_Sector" : {"lower": 1, "upper": 19},
            "User_Job_Position" : {"lower": 1, "upper": 7},
            "User_Job_Education" : {"lower": 1, "upper": 7},
            "User_Behaviour_Device" : {"lower": 1, "upper": 15}
        }

        # check
        flag, code, error = False, 200, ""

        for variable, limit in self.encoded_variables.items():
            
            if body[variable] > limit["upper"] or body[variable] < limit["lower"]:

                flag, code, error = True, 422, '''not expected values for variable {},please send a valid request with an integer number in this range: [{}, {}]'''.format(variable, limit["lower"], limit["upper"])

                return {"flag" : flag, "response" : error, "response_code" : code}

        return {"flag" : flag, "response" : error, "response_code" : code}

    def value_check_job(self, body:dict):
        
        flag, code, error = False, 200, ""

        # check user_job and User_Job_Position
        if body["User_Job_Employed"] == False and body["User_Job_Position"] != 7:

                flag, code, error = True, 422, 'not expected values for variable User_Job_Position, please insert: 7 while User_Job_Employed is false'

                return {"flag" : flag, "response" : error, "response_code" : code}
        
        elif body["User_Job_Employed"] == True and body["User_Job_Position"] == 7:
                
                flag, code, error = True, 422, 'not expected values for variable User_Job_Position, please insert: [1, 6] while User_Job_Employed is True'
                
                return {"flag" : flag, "response" : error, "response_code" : code}

        return {"flag" : flag, "response" : error, "response_code" : code}

    def value_check_japan_date_time(self, body:dict):
        
        flag, code, error = False, 200, ""

        # 1) check User_GenericInfo_Birth, and User_Behaviour_Lifetime
        variables = ["User_GenericInfo_Birth", "User_Behaviour_Lifetime"]
        for variable in variables:
            
            value = str(body[variable])

            if not len(value) == 8:
                
                flag, code, error = True, 422, 'not expected values for variable {}, please insert a value with 8 numeric characters, representing (year, month, day) like: 19800708'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

            elif (int(value[0:4]) > 2022) | (int(value[0:4]) < 1900):
                
                flag, code, error = True, 422, 'not expected values for variable {}, please insert a correct value for year, please insert a value with 8 numeric characters, representing (year, month, day) like: 19800708'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

            elif (int(value[4:6]) > 12) | (int(value[4:6]) < 1):

                flag, code, error = True, 422, 'not expected values for variable {}, please insert a correct value for month, please insert a value with 8 numeric characters, representing (year, month, day) like: 19800708'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

            elif (int(value[6:8]) > 31) | (int(value[6:8]) < 1):

                flag, code, error = True, 422, 'not expected values for variable {}, please insert a correct value for day, please insert a value with 8 numeric characters, representing (year, month, day) like: 19800708'.format(variable)

                return {"flag" : flag, "response" : error, "response_code" : code}

        # 2) check User_Behaviour_RegistrationDatetime
        variable = "User_Behaviour_RegistrationDatetime"
        value = str(body[variable])

        if not len(value) == 6:

            flag, code, error = True, 422, 'not expected values for variable {}, please insert a value with 6 numeric characters, representing (hours, minutes, seconds) like: 165353'.format(variable)

            return {"flag" : flag, "response" : error, "response_code" : code}

        elif (int(value[0:2]) > 24) | (int(value[0:2]) < 1):

            flag, code, error = True, 422, 'not expected values for variable {}, please insert a correct value for hours, please insert a value with 4 numeric characters, representing (hours, minutes, seconds) like: 165353'.format(variable)

            return {"flag" : flag, "response" : error, "response_code" : code}

        elif (int(value[2:4]) > 60) | (int(value[2:4]) < 1):

            flag, code, error = True, 422, 'not expected values for variable {}, please insert a correct value for minutes, please insert a value with 4 numeric characters, representing (hours, minutes, seconds) like: 165353'.format(variable)

            return {"flag" : flag, "response" : error, "response_code" : code}

        elif (int(value[4:6]) > 60) | (int(value[4:6]) < 1):

            flag, code, error = True, 422, 'not expected values for variable {}, please insert a correct value for seconds, please insert a value with 4 numeric characters, representing (hours, minutes, seconds) like: 165353'.format(variable)

            return {"flag" : flag, "response" : error, "response_code" : code}
        
        return {"flag" : flag, "response" : error, "response_code" : code}

    def run(self, body:dict):

        # 0)
        result = self.keys_controller_tree(body)
        if result["flag"] == True: return result

        # 1)
        body = self.ingest.body_flatener(body)

        # 2)
        result = self.type_check_int(body)
        if result["flag"] == True: return result

        # 3)
        result = self.type_check_float(body)
        if result["flag"] == True: return result

        # 4)
        result = self.type_check_bool(body)
        if result["flag"] == True: return result

        # 5)
        result = self.value_check_encoded(body)
        if result["flag"] == True: return result

        # 6)
        result = self.value_check_japan_date_time(body)
        if result["flag"] == True: return result

        # 7)
        result = self.value_check_job(body)
        if result["flag"] == True: return result

        return {"flag" : False, "response" : '', "response_code" : 200}


