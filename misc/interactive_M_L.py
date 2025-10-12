import pandas as pd
import matplotlib.pyplot as plt
from astropy.constants import M_sun, L_sun
from pathlib import Path
import numpy as np
import mplcursors

def create_plot(L, met):
    dir = Path(__file__).resolve().parent
    path = dir / "../modeling/preprocessor/output/gaia_out.csv"

    df = pd.read_csv(path)

    reg_coef = (24.49554961, 0.21843771, 0.00115995)   # From modeling on the same df: (intercept, luminosity, metallicity)

    L_scaled = np.log10(L * L_sun.value)
    M_pred = reg_coef[0] + reg_coef[1] * L_scaled + reg_coef[2] * met
    M_pred = 10**M_pred / M_sun.value

    df["M"] = 10**df["M"] / M_sun.value
    df["L"] = 10**df["L"] / L_sun.value

    df = df.drop(columns=["source_id", "met", "evolstage_flame", "Teff", "R", "spectype"])

    label_df = pd.DataFrame({
        "Name": ["\N{GREEK SMALL LETTER ALPHA} Canis Majoris A",
                 "\N{GREEK SMALL LETTER ALPHA} Piscis Austrini",
                 "Sun",
                 "\N{GREEK SMALL LETTER ALPHA} Centauri C"],
        "L": [24.7, 16.63, 1,	0.001567],
        "M": [2.06, 1.92, 1, 0.1221],
        "Info": ["Also known as Sirius, the brighest star in the night sky",
                 "Was assumed to host the first exoplanet imaged at visible\nwavelengths; it later turned out to be a dust cloud",
                 "Centerpiece of our Solar System",
                 "Our closest extrasolar neighbor"]
    })

    fig,ax = plt.subplots(figsize=(10,8))   # modify if needed

    ax.scatter(df["M"], df["L"],
                  c="black", s=30)
    ax.scatter(M_pred, L, c='red', s=80)
    diagram = ax.scatter(label_df["M"], label_df["L"],
                c="blue", s=50)
    ax.set_yscale("log")
    ax.set_ylabel(r"L (L$_\odot$)")
    ax.set_xlabel(r"M (M$_\odot$)")

    cursor = mplcursors.cursor(diagram, hover=True)
    @cursor.connect("add")
    def on_add(sel):
        idx = sel.index
        name = label_df["Name"].iloc[idx]
        info = label_df["Info"].iloc[idx]

        sel.annotation.set_text(f"$\\mathbf{{{name.replace(' ', '\\ ')}}}$\n{info}")
        sel.annotation.get_bbox_patch().set(fc="white", alpha=1)
        sel.annotation.set_fontsize(12)

    plt.show()

if __name__=="__main__":
    create_plot(10,20)