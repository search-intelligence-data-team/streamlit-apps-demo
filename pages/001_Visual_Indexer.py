from io import BytesIO, StringIO

import streamlit as st

import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis

from utils import convert_to_float, load_file, TRANSFORMATIONS, USABLE_ROW_COUNT_LIMIT

def load_excel_sheet(file_object: dict, sheet_name: str) -> pd.DataFrame:
    """
    Return a copy of the specified excel sheet as a pandas DataFrame

        Parameters:
            file_object (dict): A dict of pd.DataFrames representing excel worksheets
            sheet_name (str): The name of the excelw worksheet
        
        Returns:
            workhseet (pd.DataFrame): A pandas DataFrame copy of specified sheet
    """

    pass

if __name__ == "__main__":
    ############### Page config ###############
    st.set_page_config(
        page_title = "Visual Indexer",
        layout='wide'
    )

    st.cache_data
    def load_file_(uploaded_file: bytes) -> pd.DataFrame:
        """
        Wrapper for the load_file function in utils.py
        """
        
        return load_file(uploaded_file)
    

    st.title("Visual Indexer")

    ############### File upload ###############

    st.markdown("""---""") 
    st.subheader("File Upload")
    uploaded_file = st.file_uploader(label="Upload your excel or csv file.")

    data_df_original = load_file(uploaded_file)

    if data_df_original is not None:
        data_df_using = data_df_original.copy()
    else:
        data_df_using = None
    

    ############### Charting ###############
    if data_df_using is not None:
        st.markdown("""---""")
        st.subheader("Data Transformations")
        
        #columns_to_exclude = st.multiselect(label="Choose which columns to exclude", options=data_df_original.columns)
        #data_df_using = data_df_original.drop(columns=columns_to_exclude, axis=1)
        data_row_count = data_df_using.shape[0]

        usable_columns = []
        unusable_columns = []
        for column_name in data_df_using.columns:
            data_df_using[column_name] =  data_df_using[column_name].apply(convert_to_float)

            if data_df_using[column_name].dropna().shape[0] >= USABLE_ROW_COUNT_LIMIT:
                usable_columns.append(column_name)
            else:
                unusable_columns.append(column_name)            

        column_count = len(usable_columns)
        row_count = len(TRANSFORMATIONS.keys())

        fig, ax = plt.subplots(nrows=row_count, ncols=column_count, figsize=(50, 50))
        
        axes = ax.ravel()
        ax_num = 0
        for column_name in usable_columns:
            column_data = data_df_using[column_name].dropna().astype(float)            
            
            for k, v in TRANSFORMATIONS.items():
                #data_df_using[column].apply(v).hist(ax=axes[ax_num])
                data = column_data.apply(v)
                data.hist(ax=axes[ax_num])

                data2 = data.dropna()
                skewness_ = skew(data2)
                kurtosis_ = kurtosis(data2)
                axes[ax_num].set_title(f"{column_name}_{k}\nskew: {skewness_:.3f}, kurtosis: {kurtosis_:.3f}, obs: {len(data):,}, obs used: {len(data2):,}")
                ax_num += 1
        
        plt.tight_layout()

        if unusable_columns != []:
            st.write(f"Could not use the following column(s): {','.join([f'\'{column_name}\'' for column_name in unusable_columns])}")
        
        st.pyplot(fig)





    ############### Display raw data ###############

    if data_df_using is not None:
        st.write(data_df_using)

             


