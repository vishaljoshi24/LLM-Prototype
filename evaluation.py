import csv
import os


# Submits ratings for conversations, outputs model parameters and prompts
def submit_rating(selected_model, prompt, temperature, top_p, top_k, repetition, max_length, coherency, fluency):
    if not os.path.isfile("./evaluation.csv"):
        fields = ["model", " prompt", "temperature", "top_p", "top_k", "repetition", "max_length", "coherency", "fluency"]
        with open(r'evaluation.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
    fields = [selected_model, prompt, temperature, top_p, top_k, repetition, max_length, coherency, fluency]
    with open(r'evaluation.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
