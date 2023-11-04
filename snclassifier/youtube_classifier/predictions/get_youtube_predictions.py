#Here you will find method get_youtube_predictions(comments) which requires as imput pandas DataFrame with column "Comment". 
#As output you will get tensor with predictions, where 0 - negative comment, 1 - neutral, 2 -positive.

from fastai.text.all import *
import pandas as pd
from langdetect import detect
import re

#filepath = "snclassifier/youtube_classifier/predictions/datasets/comments.csv" 
#comments= pd.read_csv(filepath)

def preprocess_data(df):
    #delete empty rows
    df = df.dropna()
    
    #delete duplicates
    df = df.drop_duplicates()
    
    df["Comment"] = df["Comment"].tolist()
    
    #get only english comments
    def detect_language(text):
        try:
            return detect(text)
        except:
            return None  # In case of errors during language detection
    # Apply the language detection function to the 'text' column and create a new 'language' column
    df["language"] = df["Comment"].apply(detect_language)
    
    # Filter and get only rows where the detected language is English ('en')
    df = df[df['language'] == 'en']
    
    # Drop the 'language' column, you no longer need it
    df = df.drop(columns=['language'])
    
    #Clean data from hashtags,links and URLs 
    def cleaning(Comment):
        Comment = re.sub(r'#\w+','', Comment)                 # Removing Hashtags
        Comment = re.sub(r'http\S+','', Comment)              # Removing Links & URLs
        Comment = re.sub(r'@\w+','', Comment)                 # Removing Mentions
        return Comment
    
    # Defining list of Abbreviations to be expanded to its original form
    abbreviations = {'fyi': 'for your information',
                 'lol': 'laugh out loud',
                 'loza': 'laughs out loud',
                 'lmao': 'laughing',
                 'rofl': 'rolling on the floor laughing',
                 'vbg': 'very big grin',
                 'xoxo': 'hugs and kisses',
                 'xo': 'hugs and kisses',
                 'brb': 'be right back',
                 'tyt': 'take your time',
                 'thx': 'thanks',
                 'abt': 'about',
                 'bf': 'best friend',
                 'diy': 'do it yourself',
                 'faq': 'frequently asked questions',
                 'fb': 'facebook',
                 'idk': 'i don\'t know',
                 'asap': 'as soon as possible',
                 'syl': 'see you later',
                 'nvm': 'never mind',
                 'frfr':'for real for real',
                 'istg':'i swear to god',}
    
    def data_cleaning(df):
        df["Comment"] = df["Comment"].apply(cleaning)     # Calling cleaning function (1-7)
        df["Comment"] = df["Comment"].str.lower()         # Normalize all characters to lowercase
        for short_form, full_form in abbreviations.items(): # Expanding the Abbreviations
            df["Comment"] = df["Comment"].str.replace(short_form, full_form)
        return df
    #Clean data from hashtags,links and URLs 
    df = data_cleaning(df)  
    df = df.sample(frac=1, random_state=42)
    
    return df

def get_youtube_predictions(comments):
    #Load parts of trained model
    learn = load_learner('/home/nds/projects/my_snclassifier/snclassifier/youtube_classifier/predictions/saved_ml_models/ULMFiT_model.pkl')
    #preprocess imput data, load input dataframe in fastai dataloader(test_dl)
    comments = preprocess_data(comments)
    test_dl = learn.dls.test_dl(comments["Comment"])

    #Make prediction
    preds, _ = learn.get_preds(dl=test_dl)
    predicted_classes = preds.argmax(dim=1)
    #print(f" Raw predictions: {preds}")
    #print(f" Predictions after argmax: {predicted_classes}")
    #print(comments["Sentiment"])

    pred_dataframe = pd.DataFrame(predicted_classes, columns=["Preds"])
    comments["Predictions"] = pred_dataframe["Preds"]

    # Print the result

    #print(comments.columns)
    return comments

#get_youtube_predictions(comments.iloc[:10])