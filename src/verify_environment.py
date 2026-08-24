from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg2://dss150p:dss150p_lab@localhost:5432/dss150p_lab"
)

with engine.connect() as conn:
    version = conn.execute(text("SELECT version();")).scalar()
    db_name = conn.execute(text("SELECT current_database();")).scalar()
    print("PostgreSQL version:", version)
    print("Current database:", db_name)