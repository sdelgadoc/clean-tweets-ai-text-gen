import csv
import spacy

nlp = spacy.load("en_core_web_sm")


with open('538_usernames.txt_tweets.csv') as f:
    tweets = csv.reader(f)
    
    for row in tweets:
        # Filter stores tweet filter output
        # 0 = undefined, -1 = fail, 1 = pass
        filter = 0
        
        # Get the first sentence in the tweet
        doc = nlp(row[0])
        sentences = [sent.string.strip() for sent in doc.sents]
        
        # Process the first sentence in the tweet
        doc = nlp(sentences[0])
        
        ## Rule: If the subject is a person, place or thing then pass
        for token in doc:
            #print(token.text, token.pos_, token.dep_)
            if token.dep_ == "nsubj":
                if token.pos_ == "NOUN" or token.pos_ == "PROPN":
                    filter = 1

        ## Rule: If the subject is "I" or "We" then pass
        for token in doc:
            #print(token.text, token.pos_, token.dep_)
            if token.dep_ == "nsubj" and filter == 0:
                if token.text == "I" or token.pos_ == "We" or token.pos_ == "we":
                    filter = 1

        ## Rule: If the first word is a conjunction, then fail
        # Find the first token in the sentencce that is not punctuation
        for i, token in enumerate(doc):
            if token.pos_ != "PUNCT": break
                
        # If the first non-punctuoation token is a conjunction
        if doc[i].pos_ == "CCONJ" or doc[0].pos_ == "CONJ":
            filter = -1
        
        ## Rule: If the tweet starts with a dependent clause, then fail
        # Find the first token in the sentencce that is not punctuation
        for i, token in enumerate(doc):
            if token.pos_ != "PUNCT": break
        
        # Initialize flags for finding commas and subject to false
        comma_found = False
        # Iterate through sentence to find if a comma occurs before the subject
        for j, token in enumerate(doc):
            # If the token is not an initial punctuation
            if j >= i:
                if token.text == ",": comma_found = True
                
                # If the subject is found after a comman, set filter to -1
                if token.dep_ == "nsubj" and comma_found == True:
                    filter = -2
            
        ## Rule: If any of the objects of the sentence are pronouns, the fail
        for token in doc:
            if token.dep_ == "dobj" or token.dep_ == "obj":
                if token.pos_ != "PRON":
                    filter = -3
        
        if filter == -2: print(row[0])