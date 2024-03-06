import csv
import os


# Submits ratings for conversations, outputs model parameters and prompts
def submit_rating(selected_model, temperature, top_p, top_k, repetition, max_length, coherency, fluency):
    # Create the CSV if it doesn't exist
    if not os.path.isfile("./evaluation.csv"):
        fields = ["model", " prompt", "temperature", "top_p", "top_k", "repetition", "max_length", "coherency", "fluency"]
        with open(r'evaluation.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)

    # Needs to be updated with prompt collection method
    prompt=""

    # Gets all fields and stores them in evaluation.csv
    fields = [selected_model, prompt, temperature, top_p, top_k, repetition, max_length, coherency, fluency]
    with open(r'evaluation.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
