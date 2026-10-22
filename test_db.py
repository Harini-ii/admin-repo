
from sqlalchemy import text
from database import engine

with engine.connect() as connection:
    result = connection.execute(text("""
        SELECT
            column_name,
            data_type,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_schema = 'customer_hj'
          AND table_name = 'support_tickets'
        ORDER BY ordinal_position
    """))

    print("customer_hj.support_tickets columns:")

    for row in result.fetchall():
        print(row)
