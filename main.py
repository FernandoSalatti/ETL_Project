import pandas as pd
import os
import glob
from database import create_table

# variables
raw_path = 'src\\data\\raw'
excel_files = glob.glob(os.path.join(raw_path, '*.xlsx'))


# dataframes

dfs = []

if not excel_files:
    print("Not found any compatible file")

else:
    dfs
    for excel_file in excel_files:
        try:
            dfTemp = pd.read_excel(excel_file)
            file_name = os.path.basename(excel_file)

            if 'brasil' in file_name.lower():
                dfTemp['location'] = 'brazil'.upper()
            elif 'italian' in file_name.lower():
                dfTemp['location'] = 'italian'.upper()        
            elif 'france' in file_name.lower():
                dfTemp['location'] = 'france'.upper()
        
            dfTemp['campaign'] = dfTemp['utm_link'].str.extract(r'utm_campaign=(.*)')

            dfs.append(dfTemp)
            print(dfTemp)

            # Chamando a função create_table para criar a tabela no banco de dados MySQL
            table_name = file_name.split('.')[0]  # Usando o nome do arquivo como nome da tabela
            create_table(excel_file, table_name)  # Criar a tabela e inserir os dados no banco de dados

        except Exception as read_folder:
            print(f"Error during the file read : {file_name} - Error : {read_folder}")

if dfs:
    result = pd.concat(dfs, ignore_index = True)
    output_file = os.path.join('src','data', 'ready', 'TestETL.xlsx')
    writer = pd.ExcelWriter(output_file, engine = 'xlsxwriter')
    result.to_excel(writer, index=False, sheet_name='TestETL')

    writer._save()

else:
    print("Any data to save")
