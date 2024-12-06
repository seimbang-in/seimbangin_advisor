import pandas as pd
import tensorflow as tf
import json

with open('./utils/tokenizer.json','r') as f:
  tokenizer_json = json.load(f)
tokenizer_str = json.dumps(tokenizer_json)
tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_str)


print(tokenizer)