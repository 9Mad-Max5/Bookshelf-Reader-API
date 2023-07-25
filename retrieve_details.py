import json

def search_for_key(json_data, search_key):
    if isinstance(json_data, dict):
        if search_key in json_data:
            return json_data[search_key]
        else:
            for key, value in json_data.items():
                result = search_for_key(value, search_key)
                if result is not None:
                    return result
    elif isinstance(json_data, list):
        for item in json_data:
            result = search_for_key(item, search_key)
            if result is not None:
                return result
            
json_data = json.load(open("info.json"))

items = ["publisher", "isbn13", "rating", "description", "total_pages"]
items = ["publisher", "isbn13"]

for item in items:
    print(search_for_key(json_data, item))