import pandas as pd


class DataHeathCheck:
    def __init__(self, data_path):
        self.original_data = pd.read_excel(data_path, sheet_name="Original data")
        self.processed_data = pd.read_excel(data_path, sheet_name="Processed and completed data")
        self.columns_to_exclude = ['DR code', 'GTIN', 'packaging_weight_unit', 'product_weight_unit_original',
                                   'product_weight_unit', 'Material percentage check']
        self.columns_to_include = [cols for cols in self.original_data.columns if cols not in self.columns_to_exclude]

    def _verify_data(self):
        assert self.original_data['GTIN'].equals(self.processed_data['GTIN']), "Original Data GTIN values are not " \
                                                                               "same as processed values"

    def get_data(self):
        return self.original_data, self.processed_data

    # Define a function to get non-null column names for a row
    def get_non_null_columns(self, row):
        return set(row.index[row.notna()])

    # Define a function to get non-null column names for a row
    def get_null_columns(self, row):
        return set(row.index[row.isna()])

    def calculate_health_check(self):
        # Verify if the original data and processed data have same GTIN values to process
        self._verify_data()

        self.processed_data['primary_data_count'] = self.original_data[self.columns_to_include].count(
            axis=1)  # .apply(lambda x : x.count(), axis=1)
        self.processed_data['missing_data_count'] = self.processed_data[self.columns_to_include].isna().sum(
            axis=1)  # .apply(lambda x : x.isna().sum(), axis=1)
        self.processed_data['proxy_data_count'] = len(self.columns_to_include) \
                                                  - self.processed_data['primary_data_count'] \
                                                  - self.processed_data['missing_data_count']
        # Apply the function to each row
        self.processed_data['primary_data_columns'] = self.original_data[self.columns_to_include].apply(self.get_non_null_columns, axis=1)
        self.processed_data['missing_data_columns'] = self.processed_data[self.columns_to_include].apply(self.get_null_columns, axis=1)
        self.processed_data['proxy_data_columns'] = set(self.columns_to_include) - self.processed_data[
            'primary_data_columns'] - self.processed_data['missing_data_columns']

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
