import preprocessor as pp
import eda
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import re
import joblib

# Helper function to process ids for cross-referencing
def clean_ids(ids:np.ndarray):
    return  [match[0]
             if isinstance(id, str) 
             and (match := re.findall(r'\d+', id)) 
             else np.nan
             for id in ids]



#   Units after processing:
#   M: log10 of mass in kg
#   L: log10 of lum in W
#   Met:    log10 of fraction Fe/H
def main():
    dir = Path(__file__).resolve().parent
    nea_path = dir / "preprocessor/input/nea_in.csv"

    nea_raw = pd.read_csv(nea_path, comment="#")
    nea_proc = pp.NEA.process(nea_raw)

    # Retrieving gaia ids corresponding to tic ids listed in nea
    nea_ids = nea_proc["tic_id"].to_numpy()
    nea_ids = np.array(clean_ids(nea_ids))

    gaia_ids = pp.NEA.get_gaia_ids(nea_ids)

    #Quering Gaia with tic ids
    gaia_raw = pp.GAIA.get_gaia_from_ids(gaia_ids)
    gaia_proc = pp.GAIA.process(gaia_raw)

    #Join nea with gaia_ids
    nea_proc["tic_id_clean"] = nea_ids
    gaia_ids["tic_id"] = gaia_ids["tic_id"].astype(str)
    nea_proc = nea_proc.merge(gaia_ids, left_on="tic_id_clean", right_on="tic_id")

    gaia_proc = pp.GAIA.normalize_colnames(gaia_proc)
    nea_proc = pp.NEA.normalize_colnames(nea_proc)

    # gaia_proc.to_csv("gaia_out.csv", index=False)
    # nea_proc.to_csv("nea_out.csv", index=False)

    # Compare before final clean
    joined_df = pp.join_dbs(nea_proc, gaia_proc)
    eda.compare_distributions(joined_df, features=["M", "L", "Teff", "R", "met"], output_dir="eda/output")
    eda.check_missing(joined_df)

    joined_df = pp.clean_joined(joined_df)
    joined_df.to_csv("preprocessor/output/joined_out.csv", index=False)

    eda.explore(joined_df, ["M", "met", "L", "Teff", "R"], ["spectype"], output_dir="eda/output", hue_column="spectype")

    #Modelling
    #joined_path = dir / "preprocessor/output/joined_out.csv"
    #joined_df = pd.read_csv(joined_path, comment="#")
    X = joined_df[["L", "met"]] 
    M = joined_df[["M"]]

    X_train, X_test, M_train, M_test = train_test_split(X, M, test_size=0.25, random_state=1)

    model = LinearRegression()

    model.fit(X_train, M_train)
    M_pred = model.predict(X_test)

    joblib.dump(model, "linear_model.pkl")

    cv = KFold(n_splits=5, shuffle=True, random_state=1)

    r2 = np.mean(cross_val_score(model, X, M, scoring='r2', cv=cv))
    mse = -np.mean(cross_val_score(model, X, M, scoring='neg_mean_squared_error', cv=cv))
    
    print("Coefficient:", model.coef_)
    print("Intercept:", model.intercept_)
    print(f"Using regular split: \nMSE={mean_squared_error(M_test, M_pred):.3f} \nr2={r2_score(M_test, M_pred):.3f}")
    print(f"Cross validation: \nMSE={mse:.3f}, r2={r2:.3f}")



if __name__=="__main__":
    main()