import spacy
import pickle

# Load the spaCy language model
nlp = spacy.load('en_core_web_sm')

# Save the model to a file using pickle
with open('nlp_model.pkl', 'wb') as file:
    pickle.dump(nlp, file)
