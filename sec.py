import json, random, sys, requests, io, os
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

pd.set_option('display.max_columns', 100)

def getCheckBoxes(lst_input):
    '''This function looks for "X" check boxes within a list as an argument. '''
    
    checks = []
    for x in lst_input:
        if x.text == "X":
            checks.append(x.text)
        else: 
            checks.append(None)
    return checks

def getYoI(url):
    '''Year of Incorporation/Organization'''
    
    url=url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
      
    table_yoi = soup.find( "table", {"summary":"Year of Incorporation/Organization"} )
    
    yoi_box = [i for i in table_yoi.find_all("td", {"class":"CheckBox"})]
    yoi_txt = [i.text for i in table_yoi.find_all("td", {"class":"FormText"})]

    yoi_box = getCheckBoxes(lst_input=yoi_box)
    
    yoi = dict(zip(yoi_txt,yoi_box))
    
    if yoi.get("Within Last Five Years (Specify Year)") == "X":
        span = [i.text for i in table_yoi.find_all("span", {"class":"FormData"})]
        year = int(span[1])  
    else:
        year = None
    
    return year

def getInfo(url):
    ''' Principal Place of Business and Contact Information '''
    
    url = url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    table_info = soup.find( "table", {"summary":"Principal Place of Business and Contact Information"} )
    
    info_k = [i.text for i in table_info.find_all("th", {"class":"FormText"})]
    info_v = [i.text for i in table_info.find_all("td", {"class":"FormData"})]
    
    if len(info_k) != len(info_v):
        info_k = [i for i in info_k if i != "Street Address 2"]
    
    info = dict(zip(info_k,info_v))
    
    return info

def getIndustryGroup(url):
    ''' Industry Group, Agriculture '''
    
    url = url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    table_industry = soup.find( "table", {"summary":"Industry Group, Agriculture"} )

    ind_box = [i for i in table_industry.find_all("td", {"class":"CheckBox"})]

    ind_box = getCheckBoxes(lst_input=ind_box)
                
    excluded = ['Agriculture', 'Business Services','Is the issuer registered as an investment company under the Investment Company Act of 1940? ']     

    ind_txt = [i.text for i in table_industry.find_all("td", {"class":"FormText"})]
    ind_txt = [i for i in ind_txt if i not in excluded]
            
    ind = dict(zip(ind_txt,ind_box))
    ind = {k: v for k, v in ind.items() if v is not None and k not in ['Other Investment Fund','Yes','No']}
    industry= ",".join(list(ind.keys()))
    
    return industry

def getAddSEC(in_filename,out_filename):
    ''' This function gets additional SEC data from the 'linkToFillingDetails'.
        It takes in_filename' and 'out_filename' as arguments. '''

    start_time = datetime.now().replace(second=0, microsecond=0)
    
    if not os.path.exists('output'):
        os.makedirs('output')
    
    df = pd.read_csv(f"{in_filename}.csv", 
                    usecols=["cik","companyName","formType","filedAt","id","linkToFilingDetails"],
                    parse_dates=["filedAt"])

    current = 0
       
    for index, row in df.iterrows():
        
        print("Getting additional SEC data...")
        
        url = row["linkToFilingDetails"]
                
        # Year of Incorporation/Organization
        year = getYoI(url)
        df.at[index,"Year of Incorporation/Organization"] = year
          
        # Info - City        
        info = getInfo(url)
        city = (info.get("City")).title()
        df.at[index,"City"] = city
        
        # Funds
        industry = getIndustryGroup(url)
        df.at[index,"Industry Group"] = industry
        
        current += 1
        
        print("{:.2%}".format(current/len(df)))
          
    df.to_csv(f"{out_filename}.csv", index=False)
    
    end_time = datetime.now().replace(microsecond=0)
    
    print(f"Script took {end_time-start_time} to finish." )
    
    return df

if __name__ == '__main__':
  getAddSEC(in_filename="source/source",out_filename="output/output")
  
exit()


