# tools moudle 
import json

def json_write(file_name, content):
    f = open(file_name,'a')
    content = json.dumps(content, sort_keys = False, indent = 2)
    f.write(content)
    f.close()

def json_preprocess(file_name):
    f = open(file_name, 'r')
    content = eval(f.read())
    f.close()
    p_content = json.dumps(content,sort_keys = False, indent = 2)
    f = open('pre_' + file_name, 'w')
    f.write(p_content)
    f.close()





