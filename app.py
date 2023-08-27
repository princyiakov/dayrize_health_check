import streamlit as st
from src.components.data_health_check import DataHeathCheck
import plotly.express as px


def main():
    st.title("Health Check App")
    st.title("Upload File")
    uploaded_file = st.file_uploader("Upload your excel file", type=["xlsx"])

    if uploaded_file is not None:
        st.success("File Uploaded Successfully")
        # Display the Upload File section
        dhc = DataHeathCheck(uploaded_file)

        # Create tabs for navigation between Individual Records and Overall Records
        tabs = ["Overall Records", "Individual Records"]
        active_tab = st.radio("Select a page", tabs)

        if active_tab == "Overall Records":
            comparison_data = dhc.create_comparison_df()
            visualise_overall_records(comparison_data)
        elif active_tab == "Individual Records":
            data = dhc.calculate_health_check()

            individual_records_page(data)

    else:
        st.info("Please upload a Excel File to proceed")


def individual_records_page(data):
    st.title("Individual Records Visualization")

    selected_name = st.selectbox("Select a Product Name", data["Name"].unique())
    selected_data = data[data["Name"] == selected_name]

    st.subheader(f"Visualization for Product Name: {selected_name}")
    visualize_single_data(selected_data)


def visualise_overall_records(data):
    st.title("Overall Records Visualization")
    fig = px.bar(data,
                 orientation='h',
                 labels={'index': 'Columns'},
                 title='Null Value Comparison',
                 template='plotly_dark')

    fig.update_layout(barmode='stack')
    fig.update_layout(
        barmode='stack',
        height=1000,  # Adjust the height
        width=1000  # Adjust the width
    )
    st.plotly_chart(fig, use_container_width=True)


def visualize_single_data(data):
    map_colours = {"primary_data_count": "green",
                   "missing_data_count": "crimson",
                   "proxy_data_count": "orange"
                   }
    labels = ["primary_data_count", "missing_data_count", "proxy_data_count"]

    # Create Pie chart
    fig = px.pie(values=[data.primary_data_count.iloc[0], data.missing_data_count.iloc[0],
                         data.proxy_data_count.iloc[0]],
                 names=labels,
                 color=labels,
                 color_discrete_map=map_colours)

    st.plotly_chart(fig, use_container_width=True)

    primary_columns = ", ".join(list(data["primary_data_columns"].iloc[0]))
    st.markdown(
        f'<div style="background-color: green; padding: 10px; border-radius: 10px;">'
        f'<h3 style="color: white;"> Primary Data Columns provided by User</h3>'
        f'<p style="color: white;">{primary_columns}</p>'
        '</div>',
        unsafe_allow_html=True
    )

    proxy_columns = ", ".join(list(data["proxy_data_columns"].iloc[0]))
    st.markdown(
        f'<div style="background-color: orange; padding: 10px; border-radius: 10px;">'
        f'<h3 style="color: white;"> Proxy Data Columns filled by Dayrize </h3>'
        f'<p style="color: white;">{proxy_columns}</p>'
        '</div>',
        unsafe_allow_html=True
    )

    missing_columns = ", ".join(list(data["missing_data_columns"].iloc[0]))
    st.markdown(
        f'<div style="background-color: red; padding: 10px; border-radius: 10px;">'
        f'<h3 style="color: white;"> Missing Data Columns</h3>'
        f'<p style="color: white;">{missing_columns}</p>'
        '</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
