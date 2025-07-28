from sqlalchemy import create_engine
from models import Base

engine = create_engine("sqlite:///db/ferroviaria.db")

def create_all():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_all()
    print("Banco criado com sucesso!")
