import pandas as pd
from sqlalchemy import create_engine, text
import pymysql

engine = create_engine("mysql+pymysql://root:123456789@localhost:3306/ppd")

df = pd.read_sql(f"SELECT * FROM ventas_historicas LIMIT 10", con=engine)
print("\nDatos en Pandas DataFrame:")
print(df)