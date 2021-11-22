import populartimes
import json

def preJson(filename):
    f = open(filename, 'r')
    content = eval(f.read())
    f.close()
    p_content = json.dumps(content,sort_keys = False, indent = 2)
    f = open('Pre'+filename, 'w')
    f.write(p_content)
    f.close()


YOUR_API_KEY = 'AIzaSyC4DMtNlVt4fQrDry1SJU4AtwE6750x61c'

Result = populartimes.get_id(YOUR_API_KEY, "ChIJSYuuSx9awokRyrrOFTGg0GY")

ResultTxt = open('result.json', 'w')

ResultJS = json.dumps(Result)
ResultTxt.write(ResultJS)

ResultTxt.close()

preJson('result.json')
