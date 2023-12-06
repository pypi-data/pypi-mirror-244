import json
from dinkit import Recognize

reco = Recognize()

f = open('wo.json', encoding='utf-8')
strokes = json.load(f)
f.close()

print(reco.Single(strokes))