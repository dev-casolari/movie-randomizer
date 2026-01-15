import json
import pandas as pd

with open("data/movies_enriched.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

breakpoint()