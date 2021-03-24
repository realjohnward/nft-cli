import os 
from _utils import * 

t = ENV.from_string(template)
result = t.render(config=config, **vars(args))

# convert dataframes into html tables and insert them into an html template string
template_str = f'<html><head><meta name="viewport" content="width=1024"><style>{stylesheet_txt}</style></head><body>{result}</body></html>'

# Save string to html file and open it in your browser 
now_str = datetime.now().strftime("%m%d%y_%H%M")

filepath = f"./{template_name}_{now_str}.html"

with open(filepath, "w") as f:
    f.write(template_str)
    f.close()

webbrowser.open(filepath)

if prompt_save is True:
    answer = input("Save File? y or n: ")
    if answer.lower().startswith("y"):
        save = True 

if save is False:
    os.remove(filepath)



    