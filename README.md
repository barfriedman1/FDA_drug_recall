# FDA Drug Recalls Analysis Dashboard

A Streamlit web application that analyzes and visualizes FDA drug recall data in real-time using the OpenFDA API.

## Description of the project:
This interactive dashboard provides insights into drug recalls in the United States by fetching live data from the FDA's Enforcement Reports API. 
The reports are updated on a weekly basis and the data considered highly organized. 
The application categorizes recall reasons into meaningful groups and visualizes trends to help understand patterns in pharmaceutical safety issues.

### Key Features:
- **<u>Real-time data:</u>** Fetches up to 1,000 drug recalls from the OpenFDA API. (more than 1000 recalls required multiple requests (get. REST API))
- **<u>Smart categorization:</u>** Automatically groups similar recall reasons into 8 major categories
- **<u>Interactive filtering:</u>** Filter recalls by severity classification (Class I, II, or III)- as sidebar and in graph 1
- **<u>Visual analysis:</u>** Two interactive charts showing recall patterns by reason (graph 1) or over time (graph 2)
- **<u>Color-coded severity:</u>** Red (dangerous), Orange (moderate), Yellow (low risk)

### Graph 1 explanation- 8 Major Categories:
- **<u>Temperature deviation:</u>** The drug was stored or shipped outside its required temperature range, which can make it ineffective or dangerous.
- **<u>Lack of sterility assurance:</u>** Products that are supposed to be completely germ-free (sterile) might not be, or the manufacturer can't guarantee sterility. (Injectable medication, eye drops, productos for open wounds)
- **<u>Adverse reactions:</u>** Patients experienced unexpected, dangerous, or severe side effects that weren't known when the drug was approved.
- **<u>Labeling errors:</u>** Wrong, missing, or misleading information on the drug label or package.
- **<u>Incorrect potency:</u>** The drug contains the wrong amount of active ingredient - either too much or too little.
- **<u>Marketed without Approved NDA/ANDA:</u>** The company sold the drug without getting FDA approval first, which is illegal.
- **<u>Microbial contamination:</u>** The drug contains living bacteria, fungi, mold, or other microorganisms.
- **<u>Lack of process control and manufacturing defects:</u>** Problems during production that affect product quality, safety, or effectiveness. This is the broadest category covering all manufacturing-related issues.

### What Problem Does It Solve?
Drug recalls happen for many different reasons, making it hard to spot patterns. This dashboard simplifies the data by:
- Grouping hundreds of unique recall reasons into clear categories
- Showing which types of issues are most common
- Revealing trends over time
- Highlighting the most serious safety concerns

## Instructions on how to use the project:


To open the app run main.py (in pycharm execute in the Terminal Streamlit run main.py) or access online by the following link:
https://fdadrugrecall-pb3kfbfkj7nb3r7p6eqtfs.streamlit.app/