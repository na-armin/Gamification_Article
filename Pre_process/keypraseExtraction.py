import RAKE
def keyphrase_extract1(text):
    stop_dir = "../SmartStoplist.txt"
    rake_object = RAKE.Rake(stop_dir)
    # Extract keywords
    keywords = rake_object.run(text)
    return keywords


from rake_nltk import Rake
def keyphrase_extract2(text):
    rake_nltk_var = Rake()
    rake_nltk_var.extract_keywords_from_text(text)
    keyword_extracted = rake_nltk_var.get_ranked_phrases()
    return keyword_extracted

# script.py
from keybert import KeyBERT
def keyphrase_extract3(text):
    doc = text
    kw_model = KeyBERT(model='all-MiniLM-L6-v2')
    keywords = kw_model.extract_keywords(doc,keyphrase_ngram_range=(1, 5), stop_words="english",top_n=5,)
    return keywords




if __name__ == '__main__':
    # Sample text to test RAKE
    text = """Google quietly rolled out a new way for Android users to listen 
    to podcasts and subscribe to shows they like, and it already works on 
    your phone. Podcast production company Pacific Content got the exclusive 
    on it.This text is taken from Google news."""
    keywords = keyphrase_extract1(text)
    print ("keywords1: ", keywords)
    keywords = keyphrase_extract2(text)
    print("keywords2: ", keywords)
    keywords = keyphrase_extract3(text)
    print("keywords3: ", keywords)