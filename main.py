import pandas as pd
import os
import glob

# caminho para ler os arquivos
folder_path = 'src\\raw'

# lista todos os arquivos de excel
excel_files = glob.glob(os.path.join(folder_path, '*.xlsx'))

if not excel_files:
    print("Nenhum arquivo compatível encontrado")
else:

    # dataframe é uma tabela na memória para guardar o conteúdo dos arquivos
    dfs = []

    for excel_file in excel_files:
        try:
            dfTemp = pd.read_excel(excel_file)
            file_name = os.path.basename(excel_file)
            
            # criamos uma nova coluna chamada "location"
            if 'brasil' in file_name.lower():
                dfTemp['location'] = 'br'
            elif 'france' in file_name.lower():
                dfTemp['location'] = 'fr'
            elif 'italian' in file_name.lower():
                dfTemp['location'] = 'it'

            # criamos uma nova coluna chamada "campanha"
            dfTemp['campaign'] = dfTemp['utm_link'].str.extract(r'utm_campaign=(.*)')

            # guarda os dados tratados dentro de uma dataframe comum
            dfs.append(dfTemp)
            print(dfTemp)


        except Exception as e:
            print(f"Erro ao ler o arquivo{excel_file} : {e}")

if dfs:
    #concatena todas as tabelas salvas do dfs em uma unica tabela
    result = pd.concat(dfs, ignore_index=True)
    
    #caminho de saida -- também é possível renomear o arquivo de saída
    output_file = os.path.join('src', 'ready', 'AulaETL.xlsx')

    #configura o motor da escrita
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

    #leva os dados do resultado a serem escritos no motor de excel configurado
    result.to_excel(writer, index=False, sheet_name='AulaEtl')

    #salva o arquivo de excel
    writer._save()

else:
    print("nenhum dado para ser salvo")
    