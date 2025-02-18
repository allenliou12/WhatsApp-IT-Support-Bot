import pandas as pd
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)  # Set script directory as the working directory
EXISTING_FILE = os.path.join(script_dir, "Examply.xlsx")
df = pd.read_excel(EXISTING_FILE)

filtered_df = df[(df["Contact Details"] == "TH IT Allen Liou") & (df["Status"] == "Ongoing")]

print(filtered_df['Ticket No'].to_list())
