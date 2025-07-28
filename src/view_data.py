from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect
from models import Ferrovia, Patio, TerminalMercadoria

engine = create_engine('sqlite:///db/ferroviaria.db')
Session = sessionmaker(bind=engine)
session = Session()

inspector = inspect(engine)
print(inspector.get_table_names())


patios = session.query(Patio).all()
for patio in patios:
    print(f"ID: {patio.id} | Nome: {patio.name} | Código: {patio.codigo} | Em operação? {patio.em_operacao}")

ferrovia = session.query(Ferrovia).filter(Ferrovia.name == 'RMS').first()
if ferrovia:
    print(f"Ferrovia: {ferrovia.name} | Número de pátios: {len(ferrovia.patios)}")

#terminal_mercadoria = session.query(TerminalMercadoria).all()



session.close()


