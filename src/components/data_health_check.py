import pandas as pd


class DataHeathCheck:
    def __init__(self, data_path):
        self.original_data = pd.read_excel(data_path, sheet_name="Original data")
        self.processed_data = pd.read_excel(data_path, sheet_name="Processed and completed data")
        self.columns_to_exclude = ['DR code', 'GTIN', 'packaging_weight_unit', 'product_weight_unit_original',
                                   'product_weight_unit', 'Material percentage check']
        self.columns_to_include = [cols for cols in self.original_data.columns if cols not in self.columns_to_exclude]
        self.count_product_material = sum(
            col.startswith('material_') and col.endswith('_name') for col in self.processed_data.columns)
        self.count_packaging_material = sum(
            col.startswith('packaging_material_') and col.endswith('_characteristic') for col in self.processed_data.columns)

    def select_columns(self, row):
        columns_to_include = ['Name', 'Item Type', 'Brand', 'Product Weight', 'Packaging weight', 'Certification', 'Location of origin',
                              'Location of destination', 'Transport mode']  # , 'COP']
        for i in range(1, self.count_product_material + 1):
            material_name_col = f'material_{i}_name'
            material_percentage_col = f'material_{i}_percentage'
            material_characteristic_col = f'material_{i}_characteristic'
            if not pd.isna(row[material_name_col]):
                columns_to_include.extend([material_name_col, material_percentage_col, material_characteristic_col])
        for j in range(1, self.count_packaging_material + 1):
            packaging_material = f'packaging_material_{j}_name'
            packaging_weight = f'packaging_material_{j}_weight'
            packaging_characteristic = f'packaging_material_{j}_characteristic'

            if not pd.isna(row[packaging_material]):
                columns_to_include.extend([packaging_material, packaging_weight, packaging_characteristic])

        return columns_to_include

    def _verify_data(self):
        assert self.original_data['GTIN'].equals(self.processed_data['GTIN']), "Original Data GTIN values are not " \
                                                                               "same as processed values"

    def get_data(self):
        return self.original_data, self.processed_data

    # # Define a function to get non-null column names for a row
    # def get_non_null_columns(self, row):
    #     return set(row.index[row.notna()])
    #
    # # Define a function to get non-null column names for a row
    # def get_null_columns(self, row):
    #     return set(row.index[row.isna()])

    # Define a function to get non-null column names for a row
    def get_null_columns(self, row):
        row = row[row['selected_columns']]
        return set(row.index[row.isna()])

    # Define a function to get non-null column names for a row
    def get_non_null_columns(self, row):
        row = row[row['selected_columns']]
        return set(row.index[row.notna()])

    # Define a function to get non-null column names for a row
    def get_proxy_columns(self, row):
        proxy_rows = set(row['selected_columns']) - row['primary_data_columns'] - row['missing_data_columns']

        return proxy_rows

    def calculate_health_check(self):
        # Verify if the original data and processed data have same GTIN values to process
        self._verify_data()

        # Define the columns to be selected for each row based on Product and Packaging
        self.processed_data["selected_columns"] = self.processed_data.apply(self.select_columns, axis=1)
        self.original_data["selected_columns"] = self.processed_data.apply(self.select_columns, axis=1)

        self.processed_data['primary_data_columns'] = self.original_data.apply(self.get_non_null_columns, axis=1)
        self.processed_data['missing_data_columns'] = self.processed_data.apply(self.get_null_columns, axis=1)
        self.processed_data['proxy_data_columns'] = self.processed_data.apply(self.get_proxy_columns, axis=1)

        self.processed_data['primary_data_count'] = self.processed_data['primary_data_columns'].apply(lambda x: len(x))
        self.processed_data['missing_data_count'] = self.processed_data['missing_data_columns'].apply(lambda x: len(x))
        self.processed_data['proxy_data_count'] = self.processed_data['proxy_data_columns'].apply(lambda x: len(x))

        # self.processed_data['primary_data_count'] = self.original_data[self.columns_to_include].count(
        #     axis=1)  # .apply(lambda x : x.count(), axis=1)
        # self.processed_data['missing_data_count'] = self.processed_data[self.columns_to_include].isna().sum(
        #     axis=1)  # .apply(lambda x : x.isna().sum(), axis=1)
        # self.processed_data['proxy_data_count'] = len(self.columns_to_include) \
        #                                           - self.processed_data['primary_data_count'] \
        #                                           - self.processed_data['missing_data_count']
        # # Apply the function to each row
        # self.processed_data['primary_data_columns'] = self.original_data[self.columns_to_include].apply(self.get_non_null_columns, axis=1)
        # self.processed_data['missing_data_columns'] = self.processed_data[self.columns_to_include].apply(self.get_null_columns, axis=1)
        # self.processed_data['proxy_data_columns'] = set(self.columns_to_include) - self.processed_data[
        #     'primary_data_columns'] - self.processed_data['missing_data_columns']

        return self.processed_data

    def create_comparison_df(self):
        # Calculate the percentage of null values for both DataFrames
        self._verify_data()
        org_data_null_percent = (self.original_data.isnull().sum() / len(self.original_data)) * 100
        processed_data_null_percent = (self.processed_data.isnull().sum() / len(self.processed_data)) * 100

        # Create a new DataFrame to store the null value percentages
        comparison_df = pd.DataFrame({
            # 'Columns': org_data_null_percent.index,
            'org_data_null_percent': org_data_null_percent,
            'processed_data_null_percent': processed_data_null_percent,
            # 'total_null' : org_data_null_percent + processed_data_null_percent
        })
        comparison_df.fillna(0, inplace=True)
        comparison_df['total_null'] = comparison_df['org_data_null_percent'] + comparison_df[
            'processed_data_null_percent']
        comparison_df = comparison_df.sort_values(by='total_null', ascending=False)
        comparison_df.drop('total_null', inplace=True, axis=1)

        return comparison_df
