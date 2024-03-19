import csv
import os
from utils import default_model


# Submits ratings for conversations, outputs model parameters and prompts
def submit_rating(chatlog, theme, coherency, fluency, model=default_model.MODEL, temperature=default_model.TEMPERATURE,
                  top_p=default_model.TOP_P, top_k=default_model.TOP_K, repetition=default_model.REPETITION,
                  max_length=default_model.MAX_LENGTH):
    # Create the CSV if it doesn't exist
    if not os.path.isfile("../files/evaluation.csv"):
        fields = ["chatlog", "theme", "coherency", "fluency", "model", "temperature", "top_p", "top_k",
                  "repetition", "max_length"]
        with open(r'../files/evaluation.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)

    # Gets all fields and stores them in evaluation.csv
    fields = [chatlog, model, temperature, top_p, top_k, repetition, max_length, theme, coherency, fluency]
    with open(r'../files/evaluation.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
