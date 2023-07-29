# Resume Job Classification
import pickle
import pandas as pd
import resume_processor


def predict_subcategory(text_query):

    with open('./NB_model.pkl', 'rb') as file:
        model = pickle.load(file)

    column_titles = ['Database_Administrator',
                     'Front_End_Developer',
                     'Java_Developer',
                     'Network_Administrator',
                     'Project_manager',
                     'Python_Developer',
                     'Security_Analyst',
                     'Software_Developer',
                     'Systems_Administrator',
                     'Web_Developer']

    predicted_true_labels = []
    text_query = resume_processor.extract_title(text_query)
    if text_query and len(text_query) > 0:
        series_from_string = pd.Series(text_query)
        predicted_labels = model.predict(series_from_string)
        predicted_labels_array = predicted_labels.toarray()
        predicted_labels_df = pd.DataFrame(predicted_labels_array, columns=column_titles)

        for column in predicted_labels_df.columns:
            if 1 in predicted_labels_df[column].values:
                predicted_true_labels.append(column)

    return predicted_true_labels
