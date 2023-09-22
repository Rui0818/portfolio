import streamlit as st
import pandas as pd
import numpy as np
import pickle
from xgboost import XGBClassifier

# Heading of the main window

st.write("""
# Lending Club Loan Default Risk Scoring Tool

Please provide the loan information, and I will help you decide the probability of default.

""")

# Sidebar
st.sidebar.header('User Input Features')

st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/dataprofessor/data/master/penguins_example.csv)
""")

# Collects user input features into dataframe
uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    def user_input_features():
        # define the input of raw features
        purpose = st.sidebar.selectbox('Purpose',('car', 'credit_card', 'debt_consolidation', 'educational', 'home_improvement', 'house', 'major_purchase', 'medical', 'moving', 'other', 'renewable_energy', 'small_business', 'vacation', 'wedding'))
        application_type = st.sidebar.selectbox('Application Type',('Individual', 'Joint App'))
        sub_grade = st.sidebar.selectbox('Sub Grade',('A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5', 'C1', 'C2', 'C3', 'C4', 'C5', 'D1', 'D2', 'D3', 'D4', 'D5', 'E1', 'E2', 'E3', 'E4', 'E5', 'F1', 'F2', 'F3', 'F4', 'F5', 'G1', 'G2', 'G3', 'G4', 'G5'))
        home_ownership = st.sidebar.selectbox('Home Ownership',('OWN', 'RENT','MORTGAGE', 'OTHER'))
        verification_status = st.sidebar.selectbox('Verification Status',('Not Verified', 'Source Verified', 'Verified'))
        addr_state = st.sidebar.selectbox('State',('AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY'))
        initial_list_status = st.sidebar.selectbox('Initial List Status',('f', 'w'))
        
        loan_amnt= st.sidebar.number_input('loan_amnt')
        term= st.sidebar.number_input('Term')
        int_rate= st.sidebar.number_input('Interest Rate')
        fico= st.sidebar.number_input('fico')
        annual_inc= st.sidebar.number_input('Annual Income')
        dti= st.sidebar.number_input('Debt-to-Income')
        open_acc= st.sidebar.number_input('Open Accounts')
        pub_rec= st.sidebar.number_input('pub_rec')
        revol_bal= st.sidebar.number_input('revol_bal')
        revol_util= st.sidebar.number_input('revol_util')
        mort_acc= st.sidebar.number_input('mort_acc')
        pub_rec_bankruptcies= st.sidebar.number_input('pub_rec_bankruptcies')
        loan_status_flag= st.sidebar.number_input('loan_status_flag')
        
        earliest_cr_line_y= st.sidebar.number_input('earliest_cr_line_y')
        
        data = {'loan_amnt': loan_amnt,
                    'term': term,
                    'int_rate': int_rate,
                    'sub_grade': sub_grade,
                    'home_ownership': home_ownership,
                    'annual_inc': annual_inc,
                    'verification_status': verification_status,
                    'purpose': purpose,
                    'addr_state': addr_state,
                    'dti': dti,
                    'open_acc': open_acc,
                    'pub_rec': pub_rec,
                    'revol_bal': revol_bal,
                    'revol_util': revol_util,
                    'initial_list_status': initial_list_status,
                    'application_type': application_type,
                    'mort_acc': mort_acc,
                    'pub_rec_bankruptcies': pub_rec_bankruptcies,
                    'fico': fico,
                    'earliest_cr_line_y': earliest_cr_line_y}
        features = pd.DataFrame(data, index=[0])
        return data, features
    # input_df is in the raw format of input variables
    blob, input_df = user_input_features()

# handle dummy variables
# append new dummy columns in the data frame and initialize them as 0
dummy_col_list = ['sub_grade_A2','sub_grade_A3','sub_grade_A4','sub_grade_A5','sub_grade_B1','sub_grade_B2','sub_grade_B3','sub_grade_B4','sub_grade_B5','sub_grade_C1','sub_grade_C2','sub_grade_C3','sub_grade_C4','sub_grade_C5','sub_grade_D1','sub_grade_D2','sub_grade_D3','sub_grade_D4','sub_grade_D5','sub_grade_E1','sub_grade_E2','sub_grade_E3','sub_grade_E4','sub_grade_E5','sub_grade_F1','sub_grade_F2','sub_grade_F3','sub_grade_F4','sub_grade_F5','sub_grade_G1','sub_grade_G2','sub_grade_G3','sub_grade_G4','sub_grade_G5','home_ownership_OTHER','home_ownership_OWN','home_ownership_RENT','verification_status_Source Verified','verification_status_Verified','purpose_credit_card','purpose_debt_consolidation','purpose_educational','purpose_home_improvement','purpose_house','purpose_major_purchase','purpose_medical','purpose_moving','purpose_other','purpose_renewable_energy','purpose_small_business','purpose_vacation','purpose_wedding','addr_state_AL','addr_state_AR','addr_state_AZ','addr_state_CA','addr_state_CO','addr_state_CT','addr_state_DC','addr_state_DE','addr_state_FL','addr_state_GA','addr_state_HI','addr_state_IA','addr_state_ID','addr_state_IL','addr_state_IN','addr_state_KS','addr_state_KY','addr_state_LA','addr_state_MA','addr_state_MD','addr_state_ME','addr_state_MI','addr_state_MN','addr_state_MO','addr_state_MS','addr_state_MT','addr_state_NC','addr_state_ND','addr_state_NE','addr_state_NH','addr_state_NJ','addr_state_NM','addr_state_NV','addr_state_NY','addr_state_OH','addr_state_OK','addr_state_OR','addr_state_PA','addr_state_RI','addr_state_SC','addr_state_SD','addr_state_TN','addr_state_TX','addr_state_UT','addr_state_VA','addr_state_VT','addr_state_WA','addr_state_WI','addr_state_WV','addr_state_WY','initial_list_status_w','application_type_Joint App']
for col in dummy_col_list:
    input_df[col] = 0

# for each categorical variable, check its level and assign the value to dummy variables.
categorical_list = ['sub_grade',
 'home_ownership',
 'verification_status',
 'purpose',
 'addr_state',
 'initial_list_status',
 'application_type']

for var in categorical_list:
    level_name = input_df.iloc[0,:][var]
    new_col_name = var+'_'+level_name
    if new_col_name in dummy_col_list:
        input_df[new_col_name] = 1

# Drop categorical variables and 
keep_columns = ['loan_amnt','term','int_rate','annual_inc','dti','open_acc','pub_rec','revol_bal','revol_util','mort_acc','pub_rec_bankruptcies','fico','earliest_cr_line_y','sub_grade_A2','sub_grade_A3','sub_grade_A4','sub_grade_A5','sub_grade_B1','sub_grade_B2','sub_grade_B3','sub_grade_B4','sub_grade_B5','sub_grade_C1','sub_grade_C2','sub_grade_C3','sub_grade_C4','sub_grade_C5','sub_grade_D1','sub_grade_D2','sub_grade_D3','sub_grade_D4','sub_grade_D5','sub_grade_E1','sub_grade_E2','sub_grade_E3','sub_grade_E4','sub_grade_E5','sub_grade_F1','sub_grade_F2','sub_grade_F3','sub_grade_F4','sub_grade_F5','sub_grade_G1','sub_grade_G2','sub_grade_G3','sub_grade_G4','sub_grade_G5','home_ownership_OTHER','home_ownership_OWN','home_ownership_RENT','verification_status_Source Verified','verification_status_Verified','purpose_credit_card','purpose_debt_consolidation','purpose_educational','purpose_home_improvement','purpose_house','purpose_major_purchase','purpose_medical','purpose_moving','purpose_other','purpose_renewable_energy','purpose_small_business','purpose_vacation','purpose_wedding','addr_state_AL','addr_state_AR','addr_state_AZ','addr_state_CA','addr_state_CO','addr_state_CT','addr_state_DC','addr_state_DE','addr_state_FL','addr_state_GA','addr_state_HI','addr_state_IA','addr_state_ID','addr_state_IL','addr_state_IN','addr_state_KS','addr_state_KY','addr_state_LA','addr_state_MA','addr_state_MD','addr_state_ME','addr_state_MI','addr_state_MN','addr_state_MO','addr_state_MS','addr_state_MT','addr_state_NC','addr_state_ND','addr_state_NE','addr_state_NH','addr_state_NJ','addr_state_NM','addr_state_NV','addr_state_NY','addr_state_OH','addr_state_OK','addr_state_OR','addr_state_PA','addr_state_RI','addr_state_SC','addr_state_SD','addr_state_TN','addr_state_TX','addr_state_UT','addr_state_VA','addr_state_VT','addr_state_WA','addr_state_WI','addr_state_WV','addr_state_WY','initial_list_status_w','application_type_Joint App']

model_in_df = input_df[keep_columns]


# # Reads in saved classification model
load_clf = pickle.load(open('loan_xgb.pkl', 'rb'))

# Apply model to make predictions
prediction = load_clf.predict(model_in_df)
prediction_proba = load_clf.predict_proba(model_in_df)

# st.subheader('Prediction Probability')
# st.write(prediction_proba)

st.subheader('Prediction')
loan_status = np.array(['Fully Paid','Charged Off'])

# st.write(loan_status[prediction])

st.write("""
Based on the information you provided, this loan has default probability
""", 
round(prediction_proba[0][1] * 100,2), '%.', 
"""The potential outcome of this loan is """, loan_status[prediction][0],'.')

# Displays the user input features
st.subheader('Below are the features you provided:')
st.write(blob)
