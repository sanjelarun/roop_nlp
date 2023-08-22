import re
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.nn import softmax
from transformers import BertTokenizer, TFBertForSequenceClassification

physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

class BertClassifier:
    def __init__(self, model_path, num_classes):
        self.model = TFBertForSequenceClassification.from_pretrained(model_path, num_labels=num_classes)
        self.label_encoder = LabelEncoder()
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        # self.initialize_gpu()

    @staticmethod
    def initialize_gpu():
        """Dynamically allocate GPU memory."""
        physical_devices = tf.config.list_physical_devices('GPU')
        if physical_devices:
            tf.config.experimental.set_memory_growth(physical_devices[0], True)

    @staticmethod
    def load_dataset(filepath):
        """Load the dataset from the given CSV file."""
        data = []
        with open(filepath, 'r') as csvfile:
            for line in csvfile:
                if len(line) > 5:
                    a, b = line.split('",', 1)
                    a, b = a[2:], b[2:-2]
                    bs = re.findall(r"'(.*?)'", b, re.DOTALL)
                    bs = ", ".join(bs)
                    data.append((a, bs))
        return data

    def preprocess_data(self, data, num_classes):
        """Preprocess the data."""
        code = [item[0] for item in data]
        actions = [item[1] for item in data]

        df = pd.DataFrame(list(zip(code, actions)), columns=['code', 'actions'])
        return df

    def fit_label(self, df):
        self.label_encoder.fit(df['actions'])

    def predict_top_5_labels(self, code):
        """Predict the top 5 labels for a given code."""
        tokenized_input = self.tokenizer.encode(code, add_special_tokens=True, max_length=256, truncation=True, padding="max_length")
        logits = self.model.predict([tokenized_input])
        logits_values = logits.logits
        probs = softmax(logits_values)

        top_5_indices = np.argsort(probs, axis=1)[:, -5:]
        predicted_top_5_labels = [self.label_encoder.inverse_transform(indices) for indices in top_5_indices]
        return [list(indices) for indices in predicted_top_5_labels][0]

    def predict_top_class(self,code):
        tokenized_input = self.tokenizer.encode(code, add_special_tokens=True, max_length=256, truncation=True, padding="max_length")
        logits = self.model.predict([tokenized_input])
        logits_values = logits.logits
        probs = softmax(logits_values)
        # Find the class with the maximum probability
        predicted_classes = np.argmax(probs, axis=1)
        predicted_classes = self.label_encoder.inverse_transform(predicted_classes)
        return predicted_classes[0]




class Top5Predictions:
    def __init__(self):
        self.classifier = BertClassifier('nlp/model_100000_07_14.h5', 111)
        data = self.classifier.load_dataset("nlp/latest_class_10000.csv")
        df = self.classifier.preprocess_data(data, 111)
        self.classifier.fit_label(df)
    
    def make_prediction(self, code):
        return self.classifier.predict_top_5_labels(code)

top5 = Top5Predictions()
code_snap = "for num in numbers:\
count += 1"
top_5_labels = top5.make_prediction(code_snap)
top_class = top5.classifier.predict_top_class(code_snap)
print(top_5_labels)
print(top_class)
