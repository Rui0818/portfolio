import streamlit as st
import pandas as pd

st.title("Analysis on the DE-SynPUF data")
st.markdown("""
Rui Zhang 

Medicare Claims Synthetic Public Use Files (SynPUFs) were created to allow interested parties to gain familiarity using \
Medicare claims data while protecting beneficiary privacy.  The data structure of the Medicare SynPUFs is very similar \
to the CMS Limited Data Sets, but with a smaller number of variables. \
They provide data analysts and software developers the opportunity to develop programs and products utilizing the \
identical formats and variable names as those which appear in the actual CMS data files. 

This analytical tool will enables univariate and multivariable analysis on the 2008 to 2010 Inpatient Claims. It only serves \
as a demo for Rui's interview. It can be extended to more complex scenarios within the current framework.

More details about the dataset can be found on the CMS [website](https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files) \
and this [Codebook](https://www.cms.gov/files/document/de-10-codebook.pdf-0).

A quick peek on the dataset:
""")
            
schema = {
    'Beneficiary Code':str, 
    'Claim ID':str, 
    'Claim Line Segment':str, 
    'Claims start date':str, 
    'Claims end date':str,
    'Provider Institution':str, 
    'Claim Payment Amount':'Int64', 
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
    'Claim Utilization Day Count':'Int64', 
    'Inpatient discharged date':str, 
    'Claim Diagnosis Related Group Code':str
}
df = pd.read_csv("desynpuf_inpatient_simple.csv",dtype=schema)

st.write(df.head(6))
st.markdown("""
### 👈 Select a tab from the sidebar to see more analysis.
""")
# st.write(df.columns)

st.markdown("""
OR
            
### 👇 Update your own data:
""")
data = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])

