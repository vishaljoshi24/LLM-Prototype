import csv
import os


def submit_rating(selected_model, temperature, top_p, top_k, repetition, max_length, persona, informativeness,
                  coherency, fluency):
    if not os.path.isfile("./evaluation.csv"):
        fields = ["model", "temperature", "top_p", "top_k", "repetition", "max_length", "persona", "informativeness",
                  "coherency", "fluency"]
        with open(r'evaluation.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
    if informativeness:
        informativeness = 10
    else:
        informativeness = 0
    fields = [selected_model, temperature, top_p, top_k, repetition, max_length, persona, informativeness,
              coherency, fluency]
    with open(r'evaluation.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
