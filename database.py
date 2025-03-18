import pandas as pd
import os
import mysql.connector

def infer_column_type(series):

    if pd.api.types.is_numeric_dtype(series):
        return 'FLOAT'

    elif pd.api.types.is_datetime64_any_dtype(series):
        return 'DATETIME'

    else:
        return 'VARCHAR(255)'

def create_table(file_path:str, 
                 table_name: str) -> None:

    cnx = mysql.connector.connect(host='localhost',
                                  user='root',
                                  password='root',
                                  database='etl_test',
                                  auth_plugin='mysql_native_password')

    cursor = cnx.cursor()
    df = pd.read_excel(file_path)

    df = df.replace({pd.NA:None, 
                     pd.NaT: None, 
                     float('nan'):None})

    df.columns = [col.strip().replace(' ','').replace('-','').lower() for col in df.columns]


    columns = []

    for col in df.columns:

        col_type = infer_column_type(df[col])
        columns.append(f'`{col}` {col_type}')

    create_table_query = f'CREATE TABLE IF NOT EXISTS `{table_name}`({", ".join(columns)});'

    cursor.execute(create_table_query)

    for _, row in df.iterrows():

        row = row.replace({pd.NA:None, 
                           pd.NaT: None, 
                           float('nan'):None})

        placeholders = ', '.join(['%s']* len(row))

        insert_query = f'INSERT INTO {table_name}({",".join([f"`{col}`" for col in df.columns])}) VALUES ({placeholders})'

        cursor.execute(insert_query,tuple(row))

    cnx.commit()

    cursor.close()

    cnx.close()

    print(f'Tabela `{table_name}` criada e dados inseridos com sucesso!')
