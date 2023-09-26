import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

st.title('Two-Sample T-Test')
latext = r'''
- **Null Hypothesis $H_0$**: The population means of the two groups are equal, i.e., $\mu_1 = \mu_2$.
- **Alternative Hypothesis $H_a$**: The population means of the two groups are not equal, i.e., $$\mu_1 \neq \mu_2$$.

**T-Statistic**:
$$
t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}
$$
'''
st.write(latext)

@st.cache_data
def load_data():
    schema = {
    'Beneficiary Code':str, 
    'Claim ID':str, 
    'Claim Line Segment':str, 
    'Claims start date':str, 
    'Claims end date':str,
    'Provider Institution':str, 
    'Claim Payment Amount':float, 
    'NCH Primary Payer Claim Paid Amount': float, 
    'Attending Physician National Provider Identifier Number':str,
    'Operating Physician National Provider Identifier Number':str, 
    'Other Physician National Provider Identifier Number':str,
    'Inpatient admission date':str, 
    'Claim Admitting Diagnosis Code':str,
    'Claim Pass Thru Per Diem Amount':float, 
    'NCH Beneficiary Inpatient Deductible Amount':float,
    'NCH Beneficiary Part A Coinsurance Liability Amount':float,
    'NCH Beneficiary Blood Deductible Liability Amount':float,
    'Claim Utilization Day Count':float, 
    'Inpatient discharged date':str, 
    'Claim Diagnosis Related Group Code':str
    }
    df = pd.read_csv("desynpuf_inpatient_simple.csv",dtype=schema)
    return df

df = load_data()


select_col_con = ['Claim Payment Amount', 
              'Claim Utilization Day Count', 
              'Admission Duration Days',
              'NCH Primary Payer Claim Paid Amount',
              'Claim Pass Thru Per Diem Amount',
              'NCH Beneficiary Inpatient Deductible Amount']

select_col_cat = ['Provider Institution', 
              'Attending Physician National Provider Identifier Number', 
              'Claim Admitting Diagnosis Code',
              'Claim Diagnosis Related Group Code']

var_cont = st.selectbox(label='Please select a continuous variable:', options = select_col_con, index=0)
var_cat = st.selectbox(label='Please select a categorical variable:', options = select_col_cat, index=1)
select_levels = df[var_cat].unique().tolist()
var_level_1 = st.selectbox(label='Please select the first level:', options = select_levels, index=2)
var_level_2 = st.selectbox(label='Please select the second level:', options = select_levels, index=3)

st.markdown(f"""
We are going to test **{var_cont}** on two levels: **{var_cat}='{var_level_1}' vs {var_cat}='{var_level_2}'**.
""")

df_not_missing = df[~df[var_cont].isna()]
cont_level_1 = np.array(df_not_missing[df_not_missing[var_cat]==var_level_1][var_cont])
cont_level_2 = np.array(df_not_missing[df_not_missing[var_cat]==var_level_2][var_cont])
mean_level_1 = round(np.mean(cont_level_1),3)
mean_level_2 = round(np.mean(cont_level_2),3)
len_level_1 = len(cont_level_1)
len_level_2 = len(cont_level_2)

# st.write(cont_level_1[:10])

t_stat, p_value = stats.ttest_ind(cont_level_1, cont_level_2)
t_stat, p_value = round(t_stat,3), round(p_value,5)
alpha = 0.05  # Define your alpha level


st.markdown(f'#### Result Summary:')
st.write(f'Number of obs of level "{var_level_1}" = {len_level_1}')
st.write(f'Number of obs level "{var_level_2}" = {len_level_2}')
st.write(f'Mean of level "{var_level_1}" = {mean_level_1}')
st.write(f'Mean of level "{var_level_2}" = {mean_level_2}')
st.write(f'**T-statistic = {t_stat}**')
st.write(f'**P-value = {p_value}**')

if p_value < alpha:
    st.write("**Reject the null hypothesis: There is a significant difference between the means of the two samples.**")
else:
    st.write("**Fail to reject the null hypothesis: There is no significant difference between the means of the two samples.**")


# df_category = df_not_missing[var_cat].value_counts().reset_index().sort_values(by='count', ascending=False)
