import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
# Set the overall aesthetic
sns.set()
sns.set_context("talk", font_scale=0.8)  # Adjust font_scale as needed
sns.set_palette("pastel")

st.title('Univariate Visualization')
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
# st.write(df.dtypes)

select_col = ['Claim Payment Amount', 
              'Claim Utilization Day Count', 
              'Admission Duration Days',
              'NCH Primary Payer Claim Paid Amount',
              'Claim Pass Thru Per Diem Amount',
              'NCH Beneficiary Inpatient Deductible Amount']

x_axis = st.selectbox(label='Please select the variable:', options = select_col, index=0)

fig=plt.figure(figsize=(10, 4))
sns.histplot(df[x_axis], edgecolor='none', bins=18, color="skyblue")
st.pyplot(fig)

fig=plt.figure(figsize=(10, 4))
sns.ecdfplot(df[x_axis], stat='proportion', color="skyblue")
st.pyplot(fig)

st.markdown('Statistics of {}: Mean={}, p10={}, p25={}, p50={}, p75={}, p90={}.'.format(
                x_axis,
                round(df[x_axis].mean(),2), 
                round(df[x_axis].quantile(0.1), 2),
                round(df[x_axis].quantile(0.25), 2),
                round(df[x_axis].quantile(0.5), 2),
                round(df[x_axis].quantile(0.75), 2),
                round(df[x_axis].quantile(0.9), 2),
                ))