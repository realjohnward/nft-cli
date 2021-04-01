import pandas as pd 

df = pd.read_json("cryptopunks.json")



# print(records[0])

df.query('event_type == "successful"', inplace=True)

records = df.to_dict(orient='records') 
record = records[0]
for k,v in record.items(): 
    print(k, v)
    print("\n")