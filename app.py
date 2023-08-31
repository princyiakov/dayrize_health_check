# Import necessary libraries
import streamlit as st
from src.components.data_health_check import DataHeathCheck  # Importing a custom module
import plotly.express as px


# Define the main function
def main():
    # Set the title of the app
    st.title("Health Check App")
    st.title("Upload File")  # Title for the file upload section

    # Create a file uploader for Excel files
    uploaded_file = st.file_uploader("Upload your excel file", type=["xlsx"])

    if uploaded_file is not None:
        st.success("File Uploaded Successfully")  # Display a success message

        # Initialize DataHealthCheck instance with the uploaded file
        dhc = DataHeathCheck(uploaded_file)

        # Create tabs for navigation between different sections
        tabs = ["Overall Records", "Individual Records"]
        active_tab = st.radio("Select a page", tabs)  # Radio buttons for tab selection

        if active_tab == "Overall Records":
            # Calculate and display comparison data for overall records
            comparison_data = dhc.create_comparison_df()
            _, processed_data = dhc.get_data()
            data_with_health_check = dhc.calculate_health_check()
            visualise_overall_records(comparison_data, processed_data, data_with_health_check)

        elif active_tab == "Individual Records":
            # Calculate health check data for individual records and display it
            data = dhc.calculate_health_check()
            individual_records_page(data)
    else:
        st.info("Please upload an Excel File to proceed")  # Display an info message


# Function to display individual records page
def individual_records_page(data):
    st.title("Individual Records Visualization")  # Title for individual records page

    # Dropdown to select a product name
    selected_name = st.selectbox("Select a Product Name", data["Name"].unique())
    selected_data = data[data["Name"] == selected_name]

    st.subheader(f"Visualization for Product Name: {selected_name}")  # Subheader with selected product name
    visualize_single_data(selected_data)


# Function to visualize overall records
def visualise_overall_records(comparison_data, processed_data, data_with_health_check):
    st.title("Overall Records Visualization")

    visualise_average_primary_proxy_missing_piechart(data_with_health_check)
    visualise_null_value_distribution(comparison_data)
    visualise_categorical_value_distribution(processed_data)


def visualise_categorical_value_distribution(processed_data):
    st.title("Data Distribution Across Major Categorical Values")
    cat_cols = ['Brand', 'Item Type', 'COP',
                'Certification', 'material_1_name',
                'material_2_name', 'material_3_name',
                'Location of origin', 'Location of destination', 'Transport mode']
    for cols in cat_cols:
        cat_col_counts = processed_data[cols].value_counts()
        count_bar = px.bar(x=cat_col_counts.index, y=cat_col_counts.values)
        count_bar.update_layout(xaxis_title=str(cols), yaxis_title="Count")
        st.plotly_chart(count_bar, use_container_width=True)


def visualise_null_value_distribution(data):
    st.title("Null Value Comparison of Original Data vs Processed Data")  # Title for null value comparison section
    # Create a horizontal bar chart using Plotly Express
    fig_2 = px.bar(data,
                   orientation='h',
                   labels={'index': 'Columns'},
                   template='plotly_dark')
    fig_2.update_layout(barmode='stack')
    fig_2.update_layout(
        barmode='stack',
        height=1000,  # Adjust the height
        width=1000  # Adjust the width
    )
    st.plotly_chart(fig_2, use_container_width=True)


def visualise_average_primary_proxy_missing_piechart(data_with_health_check):
    st.title("Average Primary, Proxy and Missing Data Distribution")
    map_colours = {"primary_data_average_count": "green",
                   "missing_data_average_count": "crimson",
                   "proxy_data_average_count": "orange"
                   }
    labels = ["primary_data_average_count", "missing_data_average_count", "proxy_data_average_count"]
    # Overall data count
    fig_1 = px.pie(values=[data_with_health_check["primary_data_count"].mean(),
                           data_with_health_check["missing_data_count"].mean(),
                           data_with_health_check["proxy_data_count"].mean()],
                   names=labels,
                   color=labels,
                   color_discrete_map=map_colours)
    st.plotly_chart(fig_1, use_container_width=True)


# Function to visualize individual record data
def visualize_single_data(data):
    map_colours = {"primary_data_count": "green",
                   "missing_data_count": "crimson",
                   "proxy_data_count": "orange"
                   }
    labels = ["primary_data_count", "missing_data_count", "proxy_data_count"]

    # Create a pie chart using Plotly Express
    fig = px.pie(values=[data.primary_data_count.iloc[0], data.missing_data_count.iloc[0],
                         data.proxy_data_count.iloc[0]],
                 names=labels,
                 color=labels,
                 color_discrete_map=map_colours)
    st.plotly_chart(fig, use_container_width=True)

    # Display primary data columns
    primary_columns = ", ".join(list(data["primary_data_columns"].iloc[0]))
    st.markdown(
        f'<div style="background-color: green; padding: 10px; border-radius: 10px;">'
        f'<h3 style="color: white;"> Primary Data Columns provided by User</h3>'
        f'<p style="color: white;">{primary_columns}</p>'
        '</div>',
        unsafe_allow_html=True
    )

    # Display proxy data columns
    proxy_columns = ", ".join(list(data["proxy_data_columns"].iloc[0]))
    st.markdown(
        f'<div style="background-color: orange; padding: 10px; border-radius: 10px;">'
        f'<h3 style="color: white;"> Proxy Data Columns filled by Dayrize </h3>'
        f'<p style="color: white;">{proxy_columns}</p>'
        '</div>',
        unsafe_allow_html=True
    )

    # Display missing data columns
    missing_columns = ", ".join(list(data["missing_data_columns"].iloc[0]))
    st.markdown(
        f'<div style="background-color: red; padding: 10px; border-radius: 10px;">'
        f'<h3 style="color: white;"> Missing Data Columns</h3>'
        f'<p style="color: white;">{missing_columns}</p>'
        '</div>',
        unsafe_allow_html=True
    )


# Entry point of the program
if __name__ == "__main__":
    main()  # Call the main function
