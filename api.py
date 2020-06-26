import json, os, sys, random, datetime
import pandas as pd
import urllib.request

def apiPayload(page):
  ''' This Function opens and reads the query.json file. 
      It reads the defined filter parameters to send to the API.
      Once the query has been completed it writes the last page to the "form" section '''

  with open('query.json', 'r') as jsonFile: 
    payload = json.load(jsonFile)
    
    payload.update({'from': f"{page}"})
    print(f"getting page no. {page}")
  
  with open('query.json', 'w') as jsonFile:
    json.dump(payload, jsonFile )
    
  return payload
      
def apiRequest(payload):
    
  ''' This function reads the credentials. 
      Then calls the API and returns filings only for the specified query criteria.
      It takes 'payload' in JSON format as an argument. '''
        
  with open('credentials.json') as f:
    credentials = json.load(f)
  
  # API Key
  TOKEN = credentials["credentials"]["key"]
  
  # API endpoint
  API = "https://api.sec-api.io?token=" + TOKEN

  # get payload to filter parameters you want to send to the API
  payload = payload
  
  # format your payload to JSON bytes
  jsondata = json.dumps(payload)
  jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
  
  # instantiate the request 
  req = urllib.request.Request(API)

  # set the correct HTTP header: Content-Type = application/json
  req.add_header('Content-Type', 'application/json; charset=utf-8')
  # set the correct length of your request
  req.add_header('Content-Length', len(jsondataasbytes))

  # send the request to the API
  response = urllib.request.urlopen(req, jsondataasbytes)

  # read the response 
  res_body = response.read()
  
  # transform the response into JSON
  filings = json.loads(res_body.decode("utf-8"))

  # returns filings only
  return filings.get('filings')
  
  
def apiQueryToFile(filename, max_calls):
    
  ''' This function calls apiRequest and writes the source to file. 
      It takes 'filename' and 'max_calls' as arguments.'''

  if not os.path.exists('source'):
    os.makedirs('source')
  source_file = f"source/{filename}.csv"
  
  
  with open('query.json', 'r') as jsonFile:
    start = json.load(jsonFile)
    from_page_n = int(start.get('from'))
  
  for page in range(from_page_n, (max_calls-1) ):
    
    try:
      
      # get query details
      payload = apiPayload(page)

      # parse query
      data = apiRequest(payload)
  
      # load results to frame
      df = pd.DataFrame(data)
            
      with open(source_file, 'a') as f:
        df.to_csv(f, mode= 'a', index = False, encoding="utf-8", header=f.tell()==0)
      
    except:
      print(f"page no. {page} | no data")
      print("Please have a look at your API calls usage")
      pass
         
if __name__ == '__main__':
  apiQueryToFile(filename="source",max_calls=100)

exit()