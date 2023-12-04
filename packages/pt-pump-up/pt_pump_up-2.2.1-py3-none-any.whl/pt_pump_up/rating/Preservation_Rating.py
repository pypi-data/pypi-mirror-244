import requests
import pandas as pd

datasets = requests.get(f"http://pt-pump-up.inesctec.pt/api/datasets/")

if datasets.status_code != 200:
    raise Exception("Error while fetching datasets")

df = pd.DataFrame(data=datasets.json())

print(df)

"""
class PreservationRating:
    pass
"""
