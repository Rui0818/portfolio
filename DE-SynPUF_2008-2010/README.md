## Cost analysis based on DE-SynPUF data
The analysis utilizes the CMS 2008-2010 Data Entrepreneurs’ Synthetic Public Use File (DE-SynPUF). This dataset was crafted by the Centers for Medicare and Medicaid Services (CMS) to provide a means for individuals to familiarize themselves with Medicare claims data, all while ensuring the privacy of beneficiaries. This analysis focus on the medical costs. 

Centers for Medicare and Medicaid Services (CMS) is a federal agency in the US, CMS oversees the country's primary healthcare programs, including Medicare, Medicaid, and CHIP.

Medicare Claims Data refers to administrative data, also termed as Medicare Fee-for-Service claims data or health services utilization data. Managed by CMS, this data originates from payment information or bill settlements. It is clinically validated and encompasses crucial details related to care, such as admission and discharge timings, diagnostic and procedural codes, care source, date of death, and demographic specifics like age, race, ethnicity, and residence location.

CMS 2008-2010 Data Entrepreneurs’ Synthetic Public Use Files ([DE-SynPUF](https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files/cms-2008-2010-data-entrepreneurs-synthetic-public-use-file-de-synpuf)): The DE-SynPUF is a simulated version of the Medicare Claims dataset. CMS introduced the DE-SynPUF to offer a realistic claims data set to the public. While the synthetic nature of the DE-SynPUF limits its value for drawing definitive conclusions about Medicare beneficiaries, it provides a more accessible, timely, and cost-effective way to access realistic Medicare claims data. This initiative aims to foster innovation that can enhance care for beneficiaries and boost the overall health of the population. 

Due to file size limitations, each data type in the CMS Linkable 2008-2010 Medicare DE-SynPUF is released in 20 separate samples (essentially each is a .25% sample).  All claims for a particular beneficiary are in samples with the same number (i.e. all beneficiaries in sample 1 have all their claims in the sample 1 files). This analysis only uses the first partition.

Reference: Codebook [link](https://www.cms.gov/files/document/de-10-codebook.pdf-0)

## Key results

- The distribution of admission duration exhibits a right-skewed pattern. The modal value for the duration stands at 4 days. Notably, approximately 90% of the admissions span less than two weeks.

    <img src="dist_admission_duration.png" width="1000">

- The claim payments distribution demonstrates a right-skewed shape. The most frequent payment amount is \\$4000-\\$6,000. Around 90% of the claims fall below the \\$20000 mark. 

    <img src="dist_payment.png" width="1000">
