from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:cyberfusion123@localhost/cyberfusion"
)

conn = engine.connect()

print("Database Connected Successfully")

conn.close()
