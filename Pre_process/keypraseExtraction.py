import RAKE
def keyphrase_extract(text):
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

    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(doc)
    return keywords
    print(kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 5), stop_words='English',top_n=10))
    #[
    #    ('learning', 0.4604),
    #    ('algorithm', 0.4556),
    #    ('training', 0.4487),
    #    ('class', 0.4086),
    #    ('mapping', 0.3700)
    #]


if __name__ == '__main__':
    # Sample text to test RAKE
    text = """Google quietly rolled out a new way for Android users to listen 
    to podcasts and subscribe to shows they like, and it already works on 
    your phone. Podcast production company Pacific Content got the exclusive 
    on it.This text is taken from Google news."""
    keywords = keyphrase_extract(text)
    print ("keywords: ", keywords)