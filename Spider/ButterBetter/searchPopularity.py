import populartimes as pp
import json
import tools

# Populartimes_get
def get_id_to_json(API_KEY, id, out_file):
    result = pp.get_id(API_KEY,id)
    tools.json_write(out_file, result)
    return result

# Populartimes_get_method
def get_to_json(API_KEY, search_type, lower_bound, upper_bound, out_file):
    result = pp.get(API_KEY, search_type, lower_bound, upper_bound)
    tools.json_write(out_file, result)
    return result
