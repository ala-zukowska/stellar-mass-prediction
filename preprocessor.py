import numpy as np
import pandas as pd
import re

# Determines the order in which duplicates are retained
# Order: most recent comprehensive survey > older comp-
# rehensive survey > individual papers
#------------------------------------------------------
def priority(src: str):
    if re.match(r"TICv8", src):
        return 3
    elif re.match(r"Gaia DR2", src):
        return 2
    else:
        year = re.search(r"\d+", src)
        return 1 + int(year.group()) / 1e5


def process():
    hosts_df = pd.read_csv("./STELLARHOSTS_2025.09.16_23.33.38.csv", comment="#")
    
    idx = hosts_df[hosts_df["st_spectype"].str.contains(" V", na=False)].index
    
    # Dropping rows with missing data & stars not in main sequence
    hosts_df = hosts_df.iloc[idx].dropna()

    hosts_df["P"] = hosts_df["st_refname"].apply(priority)

    hosts_df = hosts_df.sort_values(["tic_id", "P"], ascending=[True, False])

    hosts_df = hosts_df.drop_duplicates(subset="tic_id", keep="first").drop(columns="P")

    # [Fe/H]: atoms of iron per atoms of hydrogen on logarithmic scale compared to the Sun
    hosts_df = hosts_df[hosts_df["st_metratio"] == "[Fe/H]"]

    hosts_df["st_mass"] = np.log10(hosts_df["st_mass"])

    hosts_df = hosts_df.drop(columns=["tic_id", "st_refname", "st_spectype", "st_metratio"])

    hosts_df.to_csv("./output.csv", index=False)
    

def main():
    process()

if __name__ == "__main__":
    main()