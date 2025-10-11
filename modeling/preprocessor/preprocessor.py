import numpy as np
import pandas as pd
import re
from astroquery.gaia import Gaia
import pyvo
from astropy.constants import M_sun, L_sun
from astropy.table import Table
from astropy.io.votable import from_table, writeto
import time

class GAIA:
    def __init__(self):
        pass

    @classmethod
    def get_gaia(cls, query:str):
        job = Gaia.launch_job_async(query)
        results = job.get_results()
        df = results.to_pandas()

        return df
    
    @classmethod
    def get_gaia_from_ids(cls, gaia_id_df: pd.DataFrame, upload_table_name: str = "gaia_ids", upload_file: str = "preprocessor/gaia_ids.xml"):
        astropy_table = Table.from_pandas(gaia_id_df)
        votable = from_table(astropy_table)
        writeto(votable, upload_file)

        query = f"""
        SELECT
            CAST(upload.gaia_dr3_id AS bigint) AS gaia_dr3_id,
            astro.mass_flame,
            astro.mh_gspphot,
            astro.lum_flame,
            astro.evolstage_flame,
            astro.teff_gspphot,
            astro.radius_gspphot,
            astro.spectraltype_esphs
        FROM tap_upload.{upload_table_name} AS upload
        JOIN gaiadr3.astrophysical_parameters AS astro
        ON CAST(upload.gaia_dr3_id AS bigint) = astro.source_id
        """

        job = Gaia.launch_job_async(query = query, upload_resource = upload_file, upload_table_name = upload_table_name, verbose=True)
        results = job.get_results()
        df = results.to_pandas()
        return df

    @classmethod
    def process(cls, df:pd.DataFrame):
        FeH_sun = 10 ** (7.46 - 12)   # source: https://www.aanda.org/articles/aa/pdf/2021/09/aa40445-21.pdf

        df["mh_gspphot"] = FeH_sun * 10**df["mh_gspphot"].astype(float)
        df["mass_flame"] = M_sun.value * df["mass_flame"].astype(float)
        df["lum_flame"] = L_sun.value * df["lum_flame"].astype(float)

        df["mh_gspphot"] = np.log10(df["mh_gspphot"])
        df["mass_flame"] = np.log10(df["mass_flame"])
        df["lum_flame"] = np.log10(df["lum_flame"])

        return df
    
    @classmethod
    def normalize_colnames(cls, df:pd.DataFrame):
        df = df.rename(columns={"mass_flame": "M", 
                                "mh_gspphot": "met", 
                                "lum_flame": "L", 
                                "teff_gspphot": "Teff", 
                                "radius_gspphot": "R", 
                                "spectraltype_esphs": "spectype"})
        return df


class NEA:
    def __init__(self):
        pass

    # Determines the order in which duplicates are retained
    # Order: most recent comprehensive survey > older comp-
    # rehensive survey > individual papers
    #------------------------------------------------------
    @classmethod
    def _priority(cls, src: str):
        if pd.isna(src):
            return 0
        elif re.match(r"TICv8", src):
            return 3
        elif re.match(r"Gaia DR2", src):
            return 2
        else:
            year = re.search(r"\d+", src)
            return 1 + int(year.group()) / 1e5 if year else 1

    @classmethod
    def get_gaia_ids(cls, ids: np.ndarray, batch_size: int = 500):
        tap = pyvo.dal.TAPService("https://mast.stsci.edu/vo-tap/api/v0.1/tic/")
        final_result = []

        for i in range(0, len(ids), batch_size):
            batch = ids[i : i+batch_size]
            id_list = ", ".join(str(x) for x in batch)

            query = f"""
            SELECT id AS tic_id, gaia AS gaia_dr3_id
            FROM dbo.catalogrecord
            WHERE ID IN ({id_list})
            """

            job = tap.submit_job(query=query)
            job.run()
            job.wait()
            query_result = job.fetch_result().to_table().to_pandas()
            final_result.append(query_result)
            print(f"Batch {i//batch_size + 1} complete")
            time.sleep(1)
        
        return pd.concat(final_result, ignore_index=True)

    @classmethod
    def process(cls, df: pd.DataFrame):
        FeH_sun = 10 ** (7.46 - 12)

        #ms_idx = df[df["st_spectype"].str.contains(" V", na=False)].index
        #df = df.iloc[ms_idx].dropna()

        df["P"] = df["st_refname"].apply(NEA._priority)
        df = df.sort_values(["tic_id", "P"], ascending=[True, False])
        df = df.drop_duplicates(subset="tic_id", keep="first").drop(columns="P")

        # Converting from solar units to SI to prevent 0s
        df = df[df["st_metratio"] == "[Fe/H]"]
        df["st_met"] = FeH_sun * 10**df["st_met"].astype(float)
        df["st_mass"] = M_sun.value * df["st_mass"].astype(float)
        df["st_lum"] = L_sun.value * 10**df["st_lum"].astype(float)

        df["st_met"] = np.log10(df["st_met"])
        df["st_mass"] = np.log10(df["st_mass"])
        df["st_lum"] = np.log10(df["st_lum"])
        df = df.drop(columns=["st_refname", "st_metratio"])

        return df
    
    @classmethod
    def normalize_colnames(cls, df:pd.DataFrame):
        df = df.rename(columns={"st_mass": "M", 
                                "st_met": "met", 
                                "st_lum": "L", 
                                "st_teff": "Teff", 
                                "st_rad": "R", 
                                "st_spectype": "spectype"})
        return df
