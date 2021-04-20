from flask import Flask,request
import requests
import io
import cv2
from PIL import Image 
import numpy as np 
import extcolors 
import json

app = Flask(__name__)



def get_color() -> str:                                                        # Returns the Dominant Color from the Image
    colors, pixel_count = extcolors.extract_from_path("new.png")
    col_str = get_hex_value(colors[0][0])
    return col_str
    

def mask_border() -> str:                                                      # Masks the Image and returns Color of the Border
    img= cv2.imread('new.png')
    cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    w ,h = int(img.shape[0]) , int(img.shape[1])
    min_ori = min(w,h)
    bw = round(0.03 * min_ori)                                                 # Width of border in pixels to masked
    mask = np.ones(img.shape[:2], dtype = "uint8")
    cv2.rectangle(mask, (bw,bw),(img.shape[1]-bw,img.shape[0]-bw), 0, -1)
    output = cv2.bitwise_and(img, img, mask = mask)
    cv2.imwrite('output.png',output)
    colors, pixel_count = extcolors.extract_from_path("output.png")

    try : 
        col_str = get_hex_value(colors[1][0])
    except :
        col_str = get_hex_value(colors[0][0])
    return col_str
    

def get_hex_value(col_tuple : tuple) -> str:
    st = '#%02X%02X%02X' %col_tuple
    return st

@app.route('/' , methods=['GET'])
def home():
    try:
        url = request.args["src"]
        data = requests.get(url)
        image = Image.open(io.BytesIO(data.content))
        image.save('new.png')                                   # Stores the Image loacally from URL 
        
        dominant_color = get_color() 
        border_color = mask_border()

        dic = dict() 
        dic['logo_border'] = border_color 
        dic['dominant_color'] = dominant_color
        
        json_data = json.dumps(dic)        
        return json_data,200
    except :
        return json.dumps({'error' : 'Invalid Parameter'}) , 400

if __name__=='__main__':
    app.run()