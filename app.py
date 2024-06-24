# Importing required libs
from keras.models import load_model
from keras.utils import img_to_array
import numpy as np
from PIL import Image
from flask import Flask, request

 
# Loading model
model = load_model("simple_playa_model.h5")
 
# Preparing and pre-processing the image
def preprocess_img(img_path):
    op_img = Image.open(img_path)
    img_resize = op_img.resize((224, 224))
    img2arr = img_to_array(img_resize) / 255.0
    img_reshape = img2arr.reshape(1, 224, 224, 3)
    return img_reshape
 
# Predicting function
def predict_result(predict):
    pred = model.predict(predict)
    return np.argmax(pred[0], axis=-1)

# Instantiating flask app
app = Flask(__name__)

@app.route('/', methods=['GET']) 
def home(): 
	return "API is running"

# Prediction route
@app.route('/predict', methods=['POST'])
def predict_image_file():
    try:
      if request.method == 'POST':
            img = preprocess_img(request.files['file'].stream)
            pred = predict_result(img)
            if pred == 0:
                  res = "home_bell"
            elif pred == 1:
                  res = "home_bulb"
            elif pred == 2:
                  res = "home_picture_frame"
            elif pred == 3:
                  res = "home_switchboard"
            else:
                  res = "home_tap"
            return {"pred": res}
 
    except:
        error = "File cannot be processed."
        return {"error": "An error"}
 
 
# Driver code
if __name__ == "__main__":
    app.run(port=5000, debug=True)