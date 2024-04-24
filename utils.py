from io import BytesIO

import numpy as np
import pandas as pd

import streamlit as st

USABLE_ROW_COUNT_LIMIT = 0.6

TRANSFORMATIONS = {
    'raw': lambda x: x,    
    'log': lambda x: np.log(x) if x > 0 else np.nan,    
    'inverse': lambda x: 1/x if x != 0 else np.nan,    
    'square_root': lambda x: np.sqrt(x) if x > 0 else np.nan,    
    #'eigth_root': lambda x: x ** 0.125 if x > 0 else np.nan,
    'squared': lambda x: x ** 2,
    #'power_four': lambda x: x ** 4
}

VALID_FILE_EXTENSIONS = [
    'csv',
    'xlsx'
]

def load_file(uploaded_file: bytes) -> pd.DataFrame:
    """
    Return a copy of the specified excel sheet as a pandas DataFrame

        Parameters:
            uploaded_file (bytes):            
        
        Returns:
            data_df (pd.DataFrame):
    """

    if uploaded_file is not None:
        file_extention = uploaded_file.name.split(".")[-1]
    else:
        file_extention = ""

    if file_extention == "":
        # no data uploaded
        data_df = None
    elif file_extention not in VALID_FILE_EXTENSIONS:
        # unsupported file type
        st.write(f"Unsupported file type '{file_extention}'. Please upload an excel or csv file.")
        data_df = None
    else:
        # load csv or excel file
        try:
            if file_extention == "csv":
                data_df = pd.read_csv(BytesIO(uploaded_file.read()))
            else:
                # get excel worksheet names
                workbook = pd.read_excel(BytesIO(uploaded_file.read()), sheet_name=None)
                sheet_name = st.selectbox(label="Select a worksheet", options=workbook.keys())

                # load excel worksheet
                if sheet_name != "":
                    data_df = workbook[sheet_name]

                    # remove empty rows
                    row = 0
                    while True:                            
                        if data_df.iloc[row].value_counts().shape[0] != 0:
                            break
                        
                        row += 1

                    column_names = list(data_df.iloc[row])
                    data_df = data_df.iloc[row + 1:].copy()
                    data_df.columns = column_names

                    if len(data_df.columns) != len(set(data_df.columns)):
                        # incorrectly formatted worksheet
                        st.write(f"Unable to read data from '{sheet_name}' worksheet. Incorrectly formatted data.")
                        data_df = None
                else:
                    data_df = None
        except AttributeError as e:
            st.write("Exception raised while loading file.")
            st.write(e)
            data_df = None

    return data_df

def convert_to_float(value: [int, float, str]):
    try:
        value_out = float(value)
    except ValueError:
        value_out = np.nan

    return value_out