import pandas as pd
import unicodedata
import os
import re

BASE_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'rawdata', 'Declaração de Rede 2025 - RMS.xlsx'))

def clean_text(texto):
    if isinstance(texto, str):
        texto = re.split(r'\(', texto)[0]
        texto = texto.strip().lower()
        texto = ''.join(
            c for c in unicodedata.normalize('NFKD', texto)
            if not unicodedata.combining(c)
        )
        return texto
    return texto

def clean_df(df):
    for col in df.select_dtypes(include='object').columns:
        df.loc[:, col] = df[col].map(clean_text)
    return df


def patio(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    columns_int = [
        'pátio',
        'código',
        'em_operação',
        'auto_assistido',
        'comprimento_útil_de_desvio_(m)',
        'tempo_médio_licenc._(min.)'
    ]

    missing = [col for col in columns_int if col not in df.columns]
    if missing:
        print(f"[!] Colunas ausentes na aba Pátios: {missing}")
        return

    df = df[columns_int]
    df = df.rename(columns={
        'comprimento_útil_de_desvio_(m)': 'comprimento_útil_desvio',
        'tempo_médio_licenc._(min.)': 'tempo_médio_licenc'
    })
    df = clean_df(df)

    patio_nomes = pd.DataFrame(df['pátio'].dropna().unique(), columns=['nome'])
    patio_nomes['id'] = patio_nomes.index + 1

    df = df.merge(patio_nomes, left_on='pátio', right_on='nome', how='left')
    if 'nome' in df.columns:
        df = df.drop(columns=['nome'])

    df.to_csv('cleandata/patios.csv', index=False)
    print("Aba Pátios processada com sucesso.")

    return patio_nomes

def entre_patios(df, patio_nomes):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    columns_int = [
        'segmento',
        'unnamed:_4',
        'linha',
    ]

    missing = [col for col in columns_int if col not in df.columns]
    if missing:
        print(f"[!] Colunas ausentes na aba Entre Pátios: {missing}")
        return

    df = df[columns_int]
    df = df.rename(columns={
        'segmento': 'patio_origem',
        'unnamed:_4': 'patio_destino'
    })
    df = clean_df(df)

    df = df.merge(patio_nomes.rename(columns={'nome': 'patio_origem'}), on='patio_origem', how='left')
    df = df.rename(columns={'id': 'patio_origem_id'})

    df = df.merge(patio_nomes.rename(columns={'nome': 'patio_destino'}), on='patio_destino', how='left')
    df = df.rename(columns={'id': 'patio_destino_id'})

    if df['patio_origem_id'].isnull().any() or df['patio_destino_id'].isnull().any():
        print("[!] Atenção: alguns pátios de origem ou destino não foram encontrados na tabela de pátios.")

    linhas = pd.DataFrame(df['linha'].dropna().unique(), columns=['nome'])
    linhas['id'] = linhas.index + 1

    df = df.merge(linhas, left_on='linha', right_on='nome', how='left')
    df = df.rename(columns={'id': 'linha_id'}).drop(columns=['linha', 'nome'])

    df_final = df[['patio_origem_id', 'patio_destino_id', 'linha_id']]
    df_final.to_csv('cleandata/entre_patios.csv', index=False)
    linhas.to_csv('cleandata/linha.csv', index=False)

    print("Aba Entre Pátios processada com sucesso.")


def terminal(df, patio_nomes):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    columns_int = [
        'pátio_de_referência',
        'terminal',
        'mercadoria',
        'capacidade',
        'unnamed:_6',
        'nº_horas_func._dia',
        'tempo_médio_de_carga',
        'unnamed:_9',
        'tempo_médio_de_descarga',
        'unnamed:_11'
    ]

    missing = [col for col in columns_int if col not in df.columns]
    if missing:
        print(f"[!] Colunas ausentes na aba Terminais: {missing}")
        return

    df = df[columns_int]
    df = df.rename(columns={
        'pátio_de_referência': 'patio_referencia',
        'capacidade': 'capacidade_vg_dia',
        'unnamed:_6': 'capacidade_tu_dia',
        'nº_horas_func._dia': 'horas_funcionamento_dia',
        'tempo_médio_de_carga': 'tempo_medio_carga_vg_h',
        'unnamed:_9': 'tempo_medio_carga_tu_h',
        'tempo_médio_de_descarga': 'tempo_medio_descarga_vg_h',
        'unnamed:_11': 'tempo_medio_descarga_tu_h'
    })
    df = clean_df(df)

    terminais = pd.DataFrame(df['terminal'].dropna().unique(), columns=['nome'])
    terminais['id'] = terminais.index + 1

    mercadorias = pd.DataFrame(df['mercadoria'].dropna().unique(), columns=['nome'])
    mercadorias['id'] = mercadorias.index + 1

    df = df.merge(terminais, left_on='terminal', right_on='nome')
    df = df.rename(columns={'id': 'terminal_id'}).drop(columns=['terminal', 'nome'])

    df = df.merge(mercadorias, left_on='mercadoria', right_on='nome')
    df = df.rename(columns={'id': 'mercadoria_id'}).drop(columns=['mercadoria', 'nome'])

    df = df.merge(patio_nomes.rename(columns={'nome': 'patio_referencia'}), on='patio_referencia', how='left')
    df = df.rename(columns={'id': 'patio_id'}).drop(columns=['patio_referencia'])

    if df['patio_id'].isnull().any():
        print("[!] Atenção: alguns pátios de referência não foram encontrados na tabela de pátios.")

    terminais.to_csv('cleandata/terminal.csv', index=False)
    mercadorias.to_csv('cleandata/mercadoria.csv', index=False)

    terminal_mercadoria = df[[
        'terminal_id',
        'mercadoria_id',
        'patio_id',
        'capacidade_vg_dia',
        'capacidade_tu_dia',
        'horas_funcionamento_dia',
        'tempo_medio_carga_vg_h',
        'tempo_medio_carga_tu_h',
        'tempo_medio_descarga_vg_h',
        'tempo_medio_descarga_tu_h'
    ]]

    terminal_mercadoria.to_csv('cleandata/terminal_mercadoria.csv', index=False)

    print("Aba Terminais processada com sucesso.")


def main():

    df_patio_raw = pd.read_excel(FILE_PATH, sheet_name=0)
    patio_nomes = patio(df_patio_raw)

    df_entre_patios = pd.read_excel(FILE_PATH, sheet_name=1)
    entre_patios(df_entre_patios, patio_nomes)
    
    df_terminal = pd.read_excel(FILE_PATH, sheet_name=4)
    terminal(df_terminal, patio_nomes)

if __name__ == "__main__":
    main()