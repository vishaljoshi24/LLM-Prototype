import pandas as pd
import random

personas_dataframe = pd.read_csv('files/personas.csv')
personas = personas_dataframe["Persona"].tolist()


def random_persona():
    return personas[random.randint(0, len(personas))]
