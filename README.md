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
* data_gothello/data_convert.py
	* Collects the winner of the game from Bart's shallow evaluated game data and converts the boards into 25 feature arrays, then adding them to a state data file. It also collects the next move as the label values and pipeling those into label files.
* data_gothello/make_data.py
	* Code suggested by the TA to convert current state data files into one-hot data. It is later used in the trainer.py and neuro_gth.py files for getting input into the neural net.
* data_gothello/one_hot.py
	* Converts the label data files into a one-hot data encoding and writes those new labels to a new file. Files have to be manually updated at the moment.

## Model training files:
* gothello-libclient-python3/model_arch.py
	* File containing the model architecture of the deep neural network using a trained weight file, it also manages data reading. Weight file is currently set to nn_3.hdf5.
* gothello-libclient-python3/trainer.py
	* File executes training of the model on the given dataset. 

## Play against the Bart AI server:
* gothello-libclient-python3/neuro_gth.py
	* Go uncomment out the client variable in neuro_gth.py with the barton server. Comment out the client variable with localhost.
    * Then run with `python3 neuro_gth.py black`

## Resources:
***Initial model architecture example:***
https://github.com/jor25/Dino_Game/blob/master/collect_states.py

***Stratify example:***
https://stackoverflow.com/questions/29438265/stratified-train-test-split-in-scikit-learn

***Sklearn train_test_split:***
https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html

***Bart’s Gothello Project:***
https://github.com/pdx-cs-ai/gothello-project

***Remove newlines from string:***
https://stackoverflow.com/questions/16566268/remove-all-line-breaks-from-a-long-string-of-text

***Split string into list:***
https://www.w3schools.com/python/python_regex.asp

***Replace specific instances:***
https://stackoverflow.com/questions/19666626/replace-all-elements-of-python-numpy-array-that-are-greater-than-some-value

***One hot my data:***
https://stackoverflow.com/questions/29831489/convert-array-of-indices-to-1-hot-encoded-numpy-array
