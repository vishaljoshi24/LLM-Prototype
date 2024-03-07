import csv
import os


# Submits ratings for conversations, outputs model parameters and prompts
def submit_rating(chatlog, model, temperature, top_p, top_k, repetition, max_length, theme, coherency, fluency):
    # Create the CSV if it doesn't exist
    if not os.path.isfile("./evaluation.csv"):
        fields = ["chatlog", "model", "temperature", "top_p", "top_k", "repetition", "max_length", "theme", "coherency",
                  "fluency"]
        with open(r'evaluation.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)

    # Gets all fields and stores them in evaluation.csv
    fields = [chatlog, model, temperature, top_p, top_k, repetition, max_length, theme, coherency, fluency]
    with open(r'evaluation.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
