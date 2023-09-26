import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
# Set the overall aesthetic
sns.set()
sns.set_context("talk", font_scale=0.8)  # Adjust font_scale as needed
sns.set_palette("pastel")
st.title('Categorical Data Visualization')
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


select_col = ['Provider Institution', 
              'Attending Physician National Provider Identifier Number', 
              'Claim Admitting Diagnosis Code',
              'Claim Diagnosis Related Group Code']

x_axis = st.selectbox(label='Please select the variable:', options = select_col, index=0)

num_category = df[x_axis].nunique()
df_category = df[x_axis].value_counts().reset_index().sort_values(by='count', ascending=False)
st.markdown(f'The variable **{x_axis}** has **{num_category}** different levels.')

if num_category < 10:
    fig=plt.figure(figsize=(10, 4))
    sns.barplot(x=x_axis, y='count', data=df_category, edgecolor='none', color="skyblue")
    st.pyplot(fig)
    st.write(df_category)

else:
    st.markdown(f'There are too many levels, we only show the top 10 levels here:')
    fig=plt.figure(figsize=(10, 4))
    sns.barplot(x=x_axis, y='count', data=df_category.head(10), edgecolor='none', color="skyblue")
    st.pyplot(fig)
    st.write(df_category.head(10))