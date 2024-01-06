import csv


def submit_rating(selected_model, temperature, top_p, top_k, repetition, max_length, persona, informativeness, coherency, fluency):
    fields = [selected_model, temperature, top_p, top_k, repetition, max_length, persona, informativeness, coherency, fluency]
    with open(r'evaluation.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
