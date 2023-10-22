#accuracy 0.835990 
from fastai.text.all import *
import pandas as pd
from langdetect import detect
import re

filepath = "backend/predictions/datasets/comments.csv" 
comments = pd.read_csv(filepath)

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
    
comment_2 = preprocess_data(comments)
df_lm = comment_2

dls_lm = DataBlock(
    blocks=TextBlock.from_df('Comment', is_lm=True),
    get_x=ColReader('text'),splitter=RandomSplitter(0.1))
dls_lm = dls_lm.dataloaders(df_lm , bs=32, seq_len=72)

learn = language_model_learner(dls_lm, AWD_LSTM, drop_mult=0.3, metrics=[accuracy]).to_fp16()

learn.fine_tune(5, 1e-2)
learn.save_encoder('finetuned')

blocks = (TextBlock.from_df('Comment', seq_len=dls_lm.seq_len, vocab=dls_lm.vocab), CategoryBlock())
dls = DataBlock(blocks=blocks,
                get_x=ColReader('text'),
                get_y=ColReader('Sentiment'),
                splitter=RandomSplitter(0.2))

dls = dls.dataloaders(comment_2, bs=32)
dls.show_batch(max_n=3)

learn_2 = text_classifier_learner(dls, AWD_LSTM, metrics=[accuracy]).to_fp16()
learn_2.load_encoder('finetuned')

learn_2.fit_one_cycle(1, 1e-2)

# Applying gradual unfreezing of one layer after another
#learn_2.freeze_to(-2)
#learn_2.fit_one_cycle(3, slice(1e-3/(2.6**4),1e-2))

learn_2.freeze_to(-3)
learn_2.fit_one_cycle(3, slice(5e-3/(2.6**4),1e-2))

learn_2.unfreeze()
learn_2.fit_one_cycle(5, slice(1e-3/(2.6**4),3e-3))

predictions = learn_2.get_preds(dl=learn_2.dls.test_dl(comment_2["Comment"].iloc[:5], bs=32)) 
predicted_classes = predictions[0].argmax(dim=1)
print(predicted_classes)

learn_2.export('backend/predictions/saved_ml_models/ULMFiT_model.pkl')