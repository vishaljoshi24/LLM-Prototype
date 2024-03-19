import csv
import os


# Submits ratings for conversations, outputs model parameters and prompts
def submit_rating(chatlog, theme, coherency, fluency, model, temperature, top_p, top_k, repetition, max_length):
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
