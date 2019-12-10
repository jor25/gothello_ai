# gothello_ai
By: ***Jordan Le*** and ***Bar Movshovich***

## Set Up:
Before running our program you must first create a virtual environment to work in. Follow the steps listed below in the order in which they appear:
* virtualenv -p python3 env
* source env/bin/activate
* pip3 install -r requirements.txt

Now you should be able to run our program. 

## Run game and nnet:
To run the game locally you will need to run two scripts that are incuded inside the repository. You will also need to open three sepearte terminals and in each one follow the steps listed below in the order in which they appear: 
##### Terminal #1
``` 
cd gothello_ai/gothello-gthd
$ sh run_local_server.sh 
```
##### Terminal #2
```
cd gothello_ai/gothello-grossthello
$ sh run_grossthello.sh 
```
##### Terminal #3
```
cd gothello_ai/gothello-libclient-python3$
python3 neuro_gth.py black
```

## data preprocessing files:
**Need to explain what each of the files below does.**
* data_gothello/data_convert.py
* data_gothello/make_data.py
* data_gothello/one_hot.py

## Model training files:
**Need to explain what each of the files below does.**
* gothello-libclient-python3/model_arch.py
* gothello-libclient-python3/trainer.py

## Play against the Bart AI server:
* gothello-libclient-python3/neuro_gth.py
