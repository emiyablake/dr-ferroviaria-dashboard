import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from models import Ferrovia, Bitola, Linha, Patio, EntrePatio, Terminal, Mercadoria, TerminalMercadoria


def insert_data(session):
    ferrovia = session.query(Ferrovia).first()
    if not ferrovia:
        ferrovia = Ferrovia(name='RMS')
        session.add(ferrovia)
        session.commit()

    bitola = session.query(Bitola).first()
    if not bitola:
        bitola = Bitola(name='Métrica')
        session.add(bitola)
        session.commit()

    df_patio = pd.read_csv('cleandata/patios.csv')
    df_entre_patios = pd.read_csv('cleandata/entre_patios.csv')
    df_linhas = pd.read_csv('cleandata/linha.csv')
    df_terminais = pd.read_csv('cleandata/terminal.csv')
    df_mercadorias = pd.read_csv('cleandata/mercadoria.csv')
    df_terminal_mercadoria = pd.read_csv('cleandata/terminal_mercadoria.csv')

    for _, row in df_patio.iterrows():
        if pd.notnull(row['pátio']):
            patio = Patio(
                name=row['pátio'],
                codigo=row.get('código'),
                em_operacao=row.get('em_operação') == 'sim',
                auto_assistido=row.get('auto_assistido') == 'sim',
                comprimento_util_desvio=row.get('comprimento_util_desvio'),
                tempo_licenciamento=row.get('tempo_licenciamento'),
                ferrovia=ferrovia
            )
            session.add(patio)
    session.commit()

    for _, row in df_linhas.iterrows():
        linha = Linha(name=row['nome'], bitola=bitola)
        session.add(linha)
    session.commit()


    for _, row in df_entre_patios.iterrows():
        if pd.notnull(row['patio_origem_id']) and pd.notnull(row['patio_destino_id']) and pd.notnull(row['linha_id']):
            ep = EntrePatio(
                idpatio_a=int(row['patio_origem_id']),
                idpatio_b=int(row['patio_destino_id']),
                idlinha=int(row['linha_id']),
                bitola=bitola
            )
            session.add(ep)

    session.commit()

    for _, row in df_terminais.iterrows():
        terminal = Terminal(name=row['nome'])
        session.add(terminal)
    session.commit()


    for _, row in df_mercadorias.iterrows():
        mercadoria = Mercadoria(name=row['nome'])
        session.add(mercadoria)
    session.commit()
    
    for _, row in df_terminal_mercadoria.iterrows():
        if pd.notnull(row['terminal_id']) and pd.notnull(row['mercadoria_id']) and pd.notnull(row['patio_id']):
            terminal_mercadoria = TerminalMercadoria(
                idterminal=int(row['terminal_id']),
                idpatio=int(row['patio_id']),
                idmercadoria=int(row['mercadoria_id']),
                capacidade_vg_dia=row.get('capacidade_vg_dia'),
                capacidade_tu_dia=row.get('capacidade_tu_dia'),
                horas_funcionamento_dia=row.get('horas_funcionamento_dia'),
                tempo_medio_carga_vg_h=row.get('tempo_medio_carga_vg_h'),
                tempo_medio_carga_tu_h=row.get('tempo_medio_carga_tu_h'),
                tempo_medio_descarga_vg_h=row.get('tempo_medio_descarga_vg_h'),
                tempo_medio_descarga_tu_h=row.get('tempo_medio_descarga_tu_h')
            )
            session.add(terminal_mercadoria)

    session.commit()

    print("Dados inseridos com sucesso!")

def main():
    engine = create_engine('sqlite:///db/ferroviaria.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    insert_data(session)

    session.close()

if __name__ == "__main__":
    main()