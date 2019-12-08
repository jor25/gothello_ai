# gothello_ai

## Set Up:
* virtualenv -p python3 env
* source env/bin/activate
* pip install numpy
* pip install keras
* pip install tensorflow
* pip install sklearn

## Run game and nnet:
`python3 neuro_gth.py black`


## data preprocessing files:
* data_gothello/data_convert.py
* data_gothello/make_data.py
* data_gothello/one_hot.py

## Model training files:
* gothello-libclient-python3/model_arch.py
* gothello-libclient-python3/trainer.py

## Play against the Bart AI server:
* gothello-libclient-python3/neuro_gth.py
