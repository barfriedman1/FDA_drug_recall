import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.title("FDA Drug Recalls Analysis", anchor=False)  # anchor=False removes the clickable link icon

# Define a function to fetch data from FDA API
# @st.cache_data caches the result so it doesn't re-fetch every time using the app
@st.cache_data
def get_data():
    response = requests.get("https://api.fda.gov/drug/enforcement.json?limit=1000")
    data = response.json() #from JSON to python

    products, classifications, reasons, years = [], [], [], []

    for recall in data['results']:
        products.append(recall.get('product_description', 'Unknown')[:50]) #unknown = default value if empty
        classifications.append(recall.get('classification', 'Unknown'))
        reasons.append(recall.get('reason_for_recall', 'Unknown'))
        report_date = recall.get('report_date', '')
        years.append(report_date[:4] if len(report_date) >= 4 else 'Unknown')

    # Create a pandas DataFrame with all the extracted data
    return pd.DataFrame({'Product': products, 'Classification': classifications,
                         'Reason': reasons, 'Year': years})


# Define a function to merge similar recall reasons into broader categories
def merge_categories(df):
    df = df.copy()  # Creates a completely independent duplicate of the dataframe, so changes to the copy don't affect the original.

    # CATEGORY 1: Lack of sterility assurance
    df.loc[df['Reason'].str.contains('sterility', case=False), 'Reason'] = 'Lack of sterility assurance'

    # CATEGORY 2: Adverse reactions
    df.loc[df['Reason'].str.contains('adverse reaction', case=False), 'Reason'] = 'Adverse reactions'

    # CATEGORY 3: Temperature deviation
    df.loc[df['Reason'].str.contains('temperature', case=False), 'Reason'] = 'Temperature deviation'

    # CATEGORY 4: Labeling errors
    for keyword in ['label', 'labeling', 'mislabel', 'mislabeling', 'misbranding', 'misbranded',
                    'packaging error', 'packaging mix', 'wrong packaging', 'incorrect packaging',
                    'package mix-up', 'packaging mix-up']:
        df.loc[df['Reason'].str.contains(keyword, case=False), 'Reason'] = 'Labeling errors'

    # CATEGORY 5: Incorrect potency
    for keyword in ['potency', 'strength', 'superpotent', 'subpotent','Potential',]:
        df.loc[df['Reason'].str.contains(keyword, case=False), 'Reason'] = 'Incorrect potency'

    # CATEGORY 6: Marketed without approved NDA/ANDA
    for keyword in ['marketed without', 'without an approved', 'unapproved', 'NDA', 'ANDA',
                    'without approved NDA', 'without approved ANDA', 'no NDA', 'no ANDA']:
        df.loc[
            df['Reason'].str.contains(keyword, case=False), 'Reason'] = 'Marketed without approved NDA/ANDA'

    # CATEGORY 7: Microbial contamination (handle ALL contamination types here)
    # First catch specific microbial terms
    for keyword in ['microbial contamination', 'bacterial contamination', 'Microbial', 'Bacterial']:
        df.loc[df['Reason'].str.contains(keyword, case=False), 'Reason'] = 'Microbial contamination'

    # CATEGORY 8: Lack of process control and Manufacturing defects (includes product contamination)
    for keyword in ['CGMP', 'manufacturing defect', 'quality', 'recalled by a supplier', 'recalled by a su',
                    'packaging defect', 'tablet defect', 'foreign particle', 'foreign matter', 'Precipitate',
                    'lack of processing control', 'stability', 'color variation', 'foreign tablet', 'foreign',
                    'dissolution', 'disintegration', 'impurities', 'impurity', 'specification', 'SOP', 'particulate ',
                    'OOS', 'out-of-specification', 'content uniformity', 'uniformity', 'pH', 'moisture',
                    'degradation product', 'nitrosamine', 'NDMA', 'NDEA', 'heavy metal', 'residue', 'imprinted',
                    'defective container', 'container defect', 'leaking container', 'container closure', 'Crystallization',
                    'chemical contamination', 'cross-contamination', 'metal','glass' ,'Particle', 'Cross contamination','Discoloration']:
        df.loc[df['Reason'].str.contains(keyword, case=False)
                                         , 'Reason'] = 'Lack of process control and Manufacturing defects'

    return df  # Return the modified dataframe


# Get data from API and merge categories
data = merge_categories(get_data())


# SIDEBAR: Create filter options on the left side of the page
st.sidebar.header("Filter Options")

# Create a dropdown menu to select classification
selected_class = st.sidebar.selectbox("Select Classification:", ['All', 'Class I', 'Class II', 'Class III'])
# Filter the data based on user selection (if 'All' selected, show all data; otherwise filter)
filtered_data = data if selected_class == 'All' else data[data['Classification'] == selected_class]
# Show how many recalls match the filter
st.sidebar.write(f"**Showing {len(filtered_data)} recalls**")
#  CLASSIFICATION SUMMARY

st.sidebar.markdown("---")  # Add separator

st.sidebar.write("**Recall Severity Classification:**")
for cls in ['Class I', 'Class II', 'Class III']:
    st.sidebar.write(f"  - {cls}: {len(data[data['Classification'] == cls])} recalls")

# GRAPH 1: Horizontal bar chart showing top 8 recall reasons
st.subheader("Graph 1: Number of Recalls by Reason", anchor=False, text_alignment='center', divider='grey')
st.badge(" 📈**Top reasons for drug recalls, colored by severity classification**", color="blue")

# Get the top 8 most common reasons from filtered data
top_8 = filtered_data['Reason'].value_counts().head(8).index
# Filter data to include only these top 8 reasons
graph1_data = filtered_data[filtered_data['Reason'].isin(top_8)]
# Group by Reason and Classification, count occurrences
reason_class = graph1_data.groupby(['Reason', 'Classification']).size().reset_index(name='Count')
# Set Classification as ordered categorical (Class I → II → III) for proper legend order
reason_class['Classification'] = pd.Categorical(reason_class['Classification'],
                                                categories=['Class I', 'Class II', 'Class III'], ordered=True)

# Show what percentage of data is displayed in the graph
st.badge(
    f" **Graph 1 displays {len(graph1_data)} out of {len(filtered_data)} recalls ({len(graph1_data) / len(filtered_data) * 100:.1f}% of data)**", icon=":material/check:", color="green")

# Create the bar chart
fig1 = px.bar(reason_class, y='Reason', x='Count', color='Classification',
              color_discrete_map={'Class I': 'red', 'Class II': 'orange', 'Class III': 'yellow'},  # Set colors
              category_orders={'Classification': ['Class I', 'Class II', 'Class III']},  # Order legend 1→2→3
              labels={'Reason': 'Reason for Recall', 'Count': 'Number of Recalls'},
              orientation='h', barmode='stack')  # Horizontal bars, stacked by classification

# Display the chart (use_container_width makes it fit the page width)
st.plotly_chart(fig1, use_container_width=True)
st.info("🖱️ Click legend to hide/show. Hover for details.")  # User instruction

# Display an info box explaining the classification system
st.info("""
**FDA Recall Classifications:**
- **Class I (Red):** Dangerous - could cause serious injury or death
- **Class II (Orange):** May cause temporary health problems
- **Class III (Yellow):** Unlikely to cause adverse health reactions
""")

st.markdown("---")  # Add separator

# GRAPH 2: Line chart showing recalls over time
st.subheader("Graph 2: Drug Recalls Over Time", anchor=False, text_alignment='center', divider='grey')
st.badge("📈**Trend of drug recalls by year**", color="blue")

# Filter out records with unknown years
year_data = filtered_data[filtered_data['Year'] != 'Unknown']
# Count how many recalls per year
year_counts = year_data['Year'].value_counts().reset_index()
year_counts.columns = ['Year', 'Count']  # Rename columns
year_counts = year_counts.sort_values('Year')  # Sort by year chronologically

# Create line chart
fig2 = px.line(year_counts, x='Year', y='Count',
               labels={'Year': 'Year', 'Count': 'Number of Recalls'}, markers=True)  # Add dots on line

# Display the chart
st.plotly_chart(fig2, use_container_width=True)
st.info("🖱️ Hover for values. Use toolbar to zoom.")  # User instruction

st.markdown("---")
st.write("Data source: FDA Recall Enforcement Reports via OpenFDA REST API")
