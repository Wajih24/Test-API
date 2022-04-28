   
import sys
import os
import shutil
import time
import traceback
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import *
from sklearn.cluster import KMeans
from lightgbm import LGBMClassifier
from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# inputs
training_data = r'dataset\Webdata_PlayerType.csv'


model_directory = 'model'
model_file_name = '%s/model_player.pickle' % model_directory
model_columns_file_name = '%s/model_columns_player.pickle' % model_directory


# These will be populated at training time
model_columns = None
clf = None


@app.route('/predict', methods=['POST'])
def predict():
   try :
      model_columns = joblib.load(model_columns_file_name)
      clf = joblib.load(model_file_name)
   except :
      model_columns = None
      model_labels = {'Playertype':{'type_achiever': 0,  'type_disruptor': 1,  'type_freeSpirit': 2,   'type_player': 3}}
      clf = None

   if clf:
      try:
         model_labels = {'Playertype':{'type_achiever': 0,  'type_disruptor': 1,  'type_freeSpirit': 2,   'type_player': 3}}
         json_ = request.json

         sample = {}
         for i in json_ :
            if i in model_columns:
               sample[i] = json_[i]
         query = pd.DataFrame(sample,index=[0])
         prediction = clf.predict(query)[0]
         lab = res = dict((v,k) for k,v in model_labels['Playertype'].items())
         return ({"prediction":lab[prediction] })

      except Exception as e:
         return jsonify({'error': str(e), 'trace': traceback.format_exc()})

   else:
        print('train first')
        return 'no model here'


@app.route('/train', methods=['GET'])
def train():
   df = pd.read_csv(training_data)
   x = df[list(joblib.load(model_columns_file_name))] 
   y = df['PlayerType_results'] 

   # capture a list of columns that will be used for prediction
   global model_columns
   model_columns = list(x.columns)
   joblib.dump(model_columns, model_columns_file_name)

   global clf
   clf = LGBMClassifier()
   start = time.time()
   clf.fit(x, y)

   joblib.dump(clf, model_file_name)

   message1 = 'Trained in %.5f seconds' % (time.time() - start)
   message2 = 'Model training score: %s' % clf.score(x, y)
   return_message = 'Success. \n{0}. \n{1}.'.format(message1, message2) 
   return ({"Message":return_message})


@app.route('/wipe', methods=['GET'])
def wipe():
    try:
        shutil.rmtree('model')
        os.makedirs(model_directory)
        return ({"Information":'Model wiped'})

    except Exception as e:
        print(str(e))
        return 'Could not remove and recreate the model directory'


if __name__ == '__main__':


    try:
        clf = joblib.load(model_file_name)
        print('model loaded')
        model_columns = joblib.load(model_columns_file_name)
        print('model columns loaded')
        

    except Exception as e:
        print('No model here')
        print('Train first')
        print(str(e))
        clf = None

    app.run(debug=True)
