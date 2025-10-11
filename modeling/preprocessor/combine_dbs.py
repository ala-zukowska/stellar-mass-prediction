import pandas as pd

def join_dbs(nea_proc: pd.DataFrame, gaia_proc: pd.DataFrame) -> pd.DataFrame:
    gaia_proc["gaia_dr3_id"] = gaia_proc["gaia_dr3_id"].astype(str)
    joined_df = nea_proc.merge(gaia_proc, on="gaia_dr3_id", suffixes=("_nea", "_gaia"))
    return joined_df

def clean_joined(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["evolstage_flame"].between(100, 360)]

    features = ["M", "L", "Teff", "R", "met"]
    for feature in features:
        df[f"{feature}_combined"] = df[f"{feature}_gaia"].combine_first(df[f"{feature}_nea"]) #Taking from gaia if not missing, else from nea
        df = df.drop(columns=[f"{feature}_nea", f"{feature}_gaia"])
    
    df= df.dropna(subset=[f"{feat}_combined" for feat in features])
    df = df[df["spectype_gaia"].str.lower() != "unknown"]

    df = df.drop(columns=["spectype_nea", "tic_id_clean", "tic_id_y", "evolstage_flame"])

    df = df.rename(columns={
        "tic_id_x": "tic_id",
        "gaia_dr3_id": "gaia_id",
        "spectype_gaia": "spectype",
        "M_combined": "M",
        "L_combined": "L",
        "Teff_combined": "Teff",
        "R_combined": "R",
        "met_combined": "met"
    })

    return df