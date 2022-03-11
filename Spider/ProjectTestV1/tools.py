# tools moudle 
import json

def json_write(filename, content):
    f = open(filename,'w')
    content = json.dumps(content)
    f.write(content)
    f.close()

def json_file_process(inputfile, outputfile):
    f = open(inputfile, 'r')
    content = eval(f.read())
    f.close()
    p_content = json.dumps(content,sort_keys = False, indent = 2)
    f = open(outputfile, 'w')
    f.write(p_content)
    f.close()



