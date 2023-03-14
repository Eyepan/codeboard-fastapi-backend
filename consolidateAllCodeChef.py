import pandas as pd
from src.database import connection

conn = connection()

for i in range(54, 81):
    df_list = []
    for j in range(ord('A'), ord('E')):
        division = chr(j)  # Get division letter
        table_name = f'codechef-START{i}{division}'
        df = pd.read_sql(f'select * from "{table_name}"', conn)
        df['division'] = division  # Add a column indicating the division
        df_list.append(df)

    combined_df = pd.concat(df_list)
    combined_table_name = f'codechef-START{i}'
    combined_df.to_sql(combined_table_name, conn,
                       if_exists='replace', index=False)

    for j in range(ord('A'), ord('E')):
        division = chr(j)
        table_name = f'codechef-START{i}{division}'
        conn.execute(f'DROP TABLE IF EXISTS "{table_name}"')
