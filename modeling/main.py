import preprocessor.preprocessor as pp
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import re

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
    # #documentation: https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_astrophysical_parameter_tables/ssec_dm_astrophysical_parameters.html

    # #astro.source_id - ID in Gaia
    # #astro.radius_gspphot - Radius
    # #astro.teff_gspphot - Effective temperature
    # #astro.mh_gspphot - Metallicity [Fe/H]
    # #astro.mass_flame - Mass
    # #astro.lum_flame - Luminosity
    # #astro.evolstage_flame - Evolutionary stage (main sequence 100-360)
    # #astro.spectraltype_esphs - Spectral type (to classify into mass ranges)

    # query = """SELECT
    #     astro.source_id,
    #     astro.mass_flame,
    #     astro.mh_gspphot,
    #     astro.lum_flame,
    #     astro.evolstage_flame,
    #     astro.teff_gspphot,
    #     astro.radius_gspphot,
    #     astro.spectraltype_esphs
    # FROM gaiadr3.astrophysical_parameters as astro
    # JOIN gaiadr3.gaia_source AS source
    # USING (source_id)
    # WHERE
    #     astro.mass_flame IS NOT NULL AND
    #     astro.mh_gspphot IS NOT NULL AND
    #     astro.lum_flame IS NOT NULL AND
    #     astro.spectraltype_esphs IS NOT NULL AND
    #     LOWER(astro.spectraltype_esphs) != 'unknown' AND
    #     astro.evolstage_flame BETWEEN 100 AND 360
    # """
    
    # gaia_raw = pp.GAIA.get_gaia(query)

    
    dir = Path(__file__).resolve().parent
    gaia_path = dir / "preprocessor/input/gaia_in.csv"
    nea_path = dir / "preprocessor/input/nea_in.csv"

    gaia_raw = pd.read_csv(gaia_path, comment="#")  # I used the first 1000 entries from the gaia table as an example input, more can be included in the final model
    nea_raw = pd.read_csv(nea_path, comment="#")

    gaia_proc = pp.GAIA.process(gaia_raw)
    nea_proc = pp.NEA.process(nea_raw)


    # Retrieving gaia ids corresponding to tic ids listed in nea
    #------------------------------------------------------
    # nea_ids = nea_proc["tic_id"].to_numpy()
    # nea_ids = np.array(clean_ids(nea_ids))

    # gaia_ids = pp.NEA.get_gaia_ids(nea_ids)

    # print(gaia_ids)
    #------------------------------------------------------

    gaia_proc = pp.GAIA.normalize_colnames(gaia_proc)
    nea_proc = pp.NEA.normalize_colnames(nea_proc)

    # gaia_proc.to_csv("gaia_out.csv", index=False)
    # nea_proc.to_csv("nea_out.csv", index=False)

    gaia_X = gaia_proc[["L", "met"]] 
    gaia_M = gaia_proc[["M"]]
    nea_X = nea_proc[["L", "met"]] 
    nea_M = nea_proc[["M"]]

    # Modeling with data from gaia dr3
    #------------------------------------------------------
    X_train, X_test, M_train, M_test = train_test_split(gaia_X, gaia_M, test_size=0.25, random_state=1)

    model = LinearRegression()
    model.fit(X_train, M_train)

    M_pred = model.predict(X_test)

    print(f"USING GAIA DR3 \n MSE={mean_squared_error(M_test, M_pred):.3f}, r2={r2_score(M_test, M_pred):.3f}") # MSE=0.001, r2=0.967

    # Modeling with data from NEA
    #------------------------------------------------------
    X_train, X_test, M_train, M_test = train_test_split(nea_X, nea_M, test_size=0.25, random_state=1)

    model = LinearRegression()
    model.fit(X_train, M_train)

    M_pred = model.predict(X_test)

    print(f"USING NEA \n MSE={mean_squared_error(M_test, M_pred):.3f}, r2={r2_score(M_test, M_pred):.3f}")  # MSE=0.018, r2=0.751


if __name__=="__main__":
    main()