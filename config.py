import json 

keys = ["mainnet_url"]

results = {}

for k in keys:
    print(f"Set value for '{k}':")
    v = input("> ")
    results[k] = v 

json.dump(results, open("./defaults.json", "w"))
print("Done")