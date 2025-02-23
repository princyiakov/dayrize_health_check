import pandas as pd


# Function to get non-null column names for a row of Original Data
def get_non_null_columns(row):
    row = row[row['selected_columns']]
    return set(row.index[row.notna()])


# Function to get null column names for a row of Processed Data
def get_null_columns(row):
    row = row[row['selected_columns']]
    return set(row.index[row.isna()])


# Function to get proxy columns (columns with non-primary and non-missing data)
def get_proxy_columns(row):
    proxy_rows = set(row['selected_columns']) - row['primary_data_columns'] - row['missing_data_columns']
    return proxy_rows


# Class to perform data health check
class DataHeathCheck:
    def __init__(self, data_path):
        # Initialize class attributes and read data from sheets
        self.original_data = pd.read_excel(data_path, sheet_name="Original data")
        self.processed_data = pd.read_excel(data_path, sheet_name="Processed and completed data")

    # Function to select relevant columns for processing based on row data
    def _select_columns(self, row):
        columns_to_include = ['Name', 'Item Type', 'Brand',
                              'COP', 'Product Weight',
                              'Packaging weight', 'Certification',
                              'Location of origin', 'Location of destination', 'Transport mode']
        # Count product and packaging material columns
        count_product_material = sum(
            col.startswith('material_') and col.endswith('_name') for col in self.processed_data.columns)
        count_packaging_material = sum(
            col.startswith('packaging_material_') and col.endswith('_characteristic') for col in
            self.processed_data.columns)

        # Include product material columns based on count
        for i in range(1, count_product_material + 1):
            material_name_col = f'material_{i}_name'
            material_percentage_col = f'material_{i}_percentage'
            material_characteristic_col = f'material_{i}_characteristic'
            if not pd.isna(row[material_name_col]):
                columns_to_include.extend([material_name_col, material_percentage_col, material_characteristic_col])

        # Include packaging material columns based on count
        for j in range(1, count_packaging_material + 1):
            packaging_material = f'packaging_material_{j}_name'
            packaging_weight = f'packaging_material_{j}_weight'
            packaging_characteristic = f'packaging_material_{j}_characteristic'
            if not pd.isna(row[packaging_material]):
                columns_to_include.extend([packaging_material, packaging_weight, packaging_characteristic])
        return columns_to_include

    # Verify that original data GTIN values match processed data GTIN values
    def _verify_data(self):
        assert self.original_data['GTIN'].equals(self.processed_data['GTIN']), "Original Data GTIN values are not " \
                                                                               "same as processed values"

    # Function to fetch the original and processed data
    def get_data(self):
        return self.original_data, self.processed_data

    # Calculate health check data
    def calculate_health_check(self):
        # Verify if the original data and processed data have the same GTIN values to process
        self._verify_data()

        # Define the columns to be selected for each row based on Product and Packaging
        self.processed_data["selected_columns"] = self.processed_data.apply(self._select_columns, axis=1)
        self.original_data["selected_columns"] = self.processed_data.apply(self._select_columns, axis=1)

        # Calculate primary, missing, and proxy data columns
        self.processed_data['primary_data_columns'] = self.original_data.apply(get_non_null_columns, axis=1)
        self.processed_data['missing_data_columns'] = self.processed_data.apply(get_null_columns, axis=1)
        self.processed_data['proxy_data_columns'] = self.processed_data.apply(get_proxy_columns, axis=1)

        # Calculate counts for primary, missing, and proxy data columns
        self.processed_data['primary_data_count'] = self.processed_data['primary_data_columns'].apply(lambda x: len(x))
        self.processed_data['missing_data_count'] = self.processed_data['missing_data_columns'].apply(lambda x: len(x))
        self.processed_data['proxy_data_count'] = self.processed_data['proxy_data_columns'].apply(lambda x: len(x))

        return self.processed_data

    # Create a comparison DataFrame for null value percentages
    def create_comparison_df(self):
        # Calculate the percentage of null values for both DataFrames
        self._verify_data()
        original_data_null_percent = (self.original_data.isnull().sum() / len(self.original_data)) * 100
        processed_data_null_percent = (self.processed_data.isnull().sum() / len(self.processed_data)) * 100

        # Create a new DataFrame to store the null value percentages
        comparison_df = pd.DataFrame({
            'original_data_null_percent': original_data_null_percent,
            'processed_data_null_percent': processed_data_null_percent,
        })
        comparison_df.fillna(0, inplace=True)
        comparison_df['total_null'] = comparison_df['original_data_null_percent'] + comparison_df[
            'processed_data_null_percent']
        comparison_df = comparison_df.sort_values(by='total_null', ascending=False)
        comparison_df.drop('total_null', inplace=True, axis=1)

        return comparison_df
