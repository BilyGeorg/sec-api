import pandas as pd
from datetime import datetime


def indexSEC(in_filename,out_filename):
  '''This function applies filters on the data, such as:
  - companies incorporated in the current year
  - belonging to any type of Pooled Investment Fund (Industry Group) 
    except Other Investment Fund.
  - limited to Form D and Form D/A filings made in the current month
  '''
  
  # date variables
  
  current_month = datetime.now().strftime("%B %Y")   
  month_start = datetime.today().replace(day=1).strftime("%Y-%m-%d")
  current_year = datetime.now().year
  
  # read file
  
  df = pd.read_csv(f"{in_filename}.csv", parse_dates=["filedAt"])
  
  # drop mising values in relevant columns
      
  df.dropna(subset=['Year of Incorporation/Organization','Industry Group'], inplace=True)

  # limited to Form D and Form D/A
  
  formType_accepted = ["D","D/A"]
  
  df = df.loc[df["formType"].isin(formType_accepted)]
  
  # belonging to any type of Pooled Investment Fund (Industry Group) except Other Investment Fund.
  
  df = df.loc[df['Industry Group'].str.contains("Fund")]
  
  # filings made in the current month
  
  df["date_filed"] = pd.to_datetime(df["filedAt"])
  
  df = df.loc[df["date_filed"] >= month_start ] 
  
  del df["date_filed"]
  
  # companies incorporated in the current year
  
  df['Year of Incorporation/Organization'] = df['Year of Incorporation/Organization'].astype(int)
  
  df = df.loc[df['Year of Incorporation/Organization'] == current_year]
  
  # format file 
  
  df["filedAt"] = pd.to_datetime(df["filedAt"]).dt.strftime("%Y-%m-%d %H:%M:%S")
  
  df.reset_index(drop=True,inplace=True)
  
  df.drop_duplicates(subset=['cik'], inplcae=True)
  
  # output file
  
  df.to_csv(f"{out_filename}_filters_applied.csv", index=False)
  
  print(f"Form D and D/A filings in {current_month} limited to Pooled Investment Fund companies incorporated in {current_year}:\nTotal number: {len(df)}")

  return df

if __name__ == '__main__':  
  indexSEC(in_filename="output/output",out_filename="output/final_output")

exit()