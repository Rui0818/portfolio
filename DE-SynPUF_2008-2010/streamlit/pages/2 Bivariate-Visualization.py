import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
# Set the overall aesthetic
sns.set()
sns.set_context("talk", font_scale=0.8)  # Adjust font_scale as needed
sns.set_palette("pastel")
st.title('Bi-variate Visualization')
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


select_col = ['Claim Payment Amount', 
              'Claim Utilization Day Count', 
              'Admission Duration Days',
              'NCH Primary Payer Claim Paid Amount',
              'Claim Pass Thru Per Diem Amount',
              'NCH Beneficiary Inpatient Deductible Amount']

st.write('Please make selections for the scatter plot')
x_axis = st.selectbox(label='X-axis:', options = select_col, index=0)
y_axis = st.selectbox(label='Y-axis:', options = select_col, index=1)


fig=plt.figure(figsize=(10, 4))
ax = sns.scatterplot(x=df[x_axis],y=df[y_axis],alpha=0.7, edgecolor='none', color="skyblue",s=20)
ax.set_xlabel(x_axis)
ax.set_ylabel(y_axis)
ax.set_title('Scatter Plot: {} vs. {}'.format(x_axis, y_axis))
st.pyplot(fig)

st.write(f'**Pearson Correlation Coeffient={round(df[x_axis].corr(df[y_axis]),3)}**')