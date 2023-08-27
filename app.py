import streamlit as st
from src.components.data_health_check import DataHeathCheck
import plotly.express as px
#
# def main():
#     st.title("Data Health Check")
#
#     uploaded_file = st.file_uploader("Upload your excel file", type=["xlsx"])
#
#     if uploaded_file is not None:
#         dhc = DataHeathCheck(uploaded_file)
#         st.success("File Uploaded Successfully")
#
#         st.write("Redirecting to Visualisation")
#         data = dhc.calculate_health_check()
#         show_visualisation(data)
#     else:
#         st.info("Please upload a Excel File to proceed")
#
#
# def show_visualisation(data):
#     st.title("Data Visualisation")
#
#     # Create a dropdown widget for selecting a value from the "Name" column
#     selected_name = st.sidebar.selectbox("Select a Product Name", data["Name"].unique())
#
#     # Select Dataframe
#     selected_data = data[data["Name"] == selected_name]
#     count_df = selected_data[["primary_data_count", "missing_data_count", "proxy_data_count"]]
#     # Define custom colors for each section
#     custom_colors = {
#         "primary_data_count": "green",
#         "missing_data_count": "red",
#         "proxy_data_count": "yellow"
#     }
#     # Create Pie chart
#     st.subheader("Pie Chart for Product Name : ", selected_name)
#     fig = px.pie(values=[selected_data.primary_data_count.iloc[0], selected_data.missing_data_count.iloc[0],
#                          selected_data.proxy_data_count.iloc[0]],
#                  names=["primary_data_count", "missing_data_count", "proxy_data_count"],
#                  color_discrete_map=custom_colors)
#     # fig = px.pie(count_df,
#     #              values=count_df.values,
#     #              names=count_df.index
#     #              )
#     #st.plotly_chart(fig, use_container_width=True)
#     st.write(fig)
#     # st.markdown(
#     #     f'<div style="background-color: red; padding: 10px; border-radius: 10px;">'
#     #     f'<h2 style="color: white;">{str(selected_data["missing_data_columns"])}</h2>'
#     #     f'<p style="color: white;">This is some information about {selected_data["missing_data_columns"]}</p>'
#     #     '</div>',
#     #     unsafe_allow_html=True
#     # )
#
# # import streamlit as st
# # import random
# #
# # # Function to generate a random color
# # def get_random_color():
# #     color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
# #     return color
# #
# # def main():
# #     st.title("List of Names with Colorful Blocks")
# #
# #     names = [
# #         "John Doe",
# #         "Jane Smith",
# #         "Michael Johnson",
# #         "Emily Brown",
# #         "William Davis"
# #     ]
# #
# #     for name in names:
# #         # Generate a random background color for each name block
# #         background_color = get_random_color()
# #
# #         # Apply the color to a styled div
# #         st.markdown(
# #             f'<div style="background-color: red; padding: 10px; border-radius: 10px;">'
# #             f'<h2 style="color: white;">{name}</h2>'
# #             f'<p style="color: white;">This is some information about {name}</p>'
# #             '</div>',
# #             unsafe_allow_html=True
# #         )
# #
# if __name__ == "__main__":
#     main()
import streamlit as st
import pandas as pd
import plotly.express as px


# # Sample data for demonstration
# data = pd.DataFrame({
#     "Name": ["Product A", "Product B", "Product C"],
#     "primary_data_count": [100, 150, 200],
#     "missing_data_count": [10, 20, 30],
#     "proxy_data_count": [5, 10, 15]
# })


def main():
    st.title("Data Visualization App")
    st.title("Upload File")
    uploaded_file = st.file_uploader("Upload your excel file", type=["xlsx"])

    if uploaded_file is not None:
        st.success("File Uploaded Successfully")
        # Display the Upload File section
        dhc = DataHeathCheck(uploaded_file)
        data = dhc.calculate_health_check()

        # Create tabs for navigation between Individual Records and Overall Records
        tabs = ["Individual Records", "Overall Records"]
        active_tab = st.radio("Select a page", tabs)

        if active_tab == "Individual Records":
            individual_records_page(data)
        elif active_tab == "Overall Records":
            overall_records_page(data)

    else:
        st.info("Please upload a Excel File to proceed")


def individual_records_page(data):
    st.title("Individual Records Visualization")

    selected_name = st.selectbox("Select a Product Name", data["Name"].unique())
    selected_data = data[data["Name"] == selected_name]

    st.subheader(f"Visualization for Product Name: {selected_name}")
    visualize_data(selected_data)


def overall_records_page(data):
    st.title("Overall Records Visualization")
    visualize_data(data)


def visualize_data(data):
    # Define custom colors for each section
    custom_colors = {
        "primary_data_count": "green",
        "missing_data_count": "red",
        "proxy_data_count": "yellow"
    }
    # Create Pie chart
    fig = px.pie(values=[data.primary_data_count.iloc[0], data.missing_data_count.iloc[0],
                         data.proxy_data_count.iloc[0]],
                 names=["primary_data_count", "missing_data_count", "proxy_data_count"],
                 color_discrete_map=custom_colors)

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
