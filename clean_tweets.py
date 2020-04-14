import csv
import spacy

nlp = spacy.load("en_core_web_sm")


with open('538_usernames.txt_tweets.csv') as f:
    spamreader = csv.reader(f)
    
    for row in spamreader:
        # Filter stores tweet filter output
        # 0 = undefined, -1 = fail, 1 = pass
        filter = 0
        
        # Get the first sentence in the tweet
        doc = nlp(row[0])
        sentences = [sent.string.strip() for sent in doc.sents]
        
        # Process the first sentence in the tweet
        doc = nlp(sentences[0])
        
        # Rule: If the subject is a person, place or thing then pass
        for token in doc:
            #print(token.text, token.pos_, token.dep_)
            if token.dep_ == "nsubj":
                if token.pos_ == "NOUN" or token.pos_ == "PROPN":
                    filter = 1

        # Rule: If the subject is "I" or "We" then pass
        for token in doc:
            #print(token.text, token.pos_, token.dep_)
            if token.dep_ == "nsubj" and filter == 0:
                if token.text == "I" or token.pos_ == "We" or token.pos_ == "we":
                    filter = 1

        # Rule: If the first word is a conjunction, then fail
        # Find the first token that is not punctuation
        i = 0
        while doc[i].pos_ == "PUNCT":
            i = i + 1
        # If the first non-punctuoation token is a conjunction
        if doc[i].pos_ == "CCONJ" or doc[0].pos_ == "CONJ":
            filter = -1
        
        print(row[0])
        print(filter)
        i = 0