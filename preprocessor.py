import numpy as np
import pandas as pd
import re
from astroquery.gaia import Gaia

def get_gaia():
    #documentation: https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_astrophysical_parameter_tables/ssec_dm_astrophysical_parameters.html

    #astro.source_id - ID in Gaia
    #astro.radius_gspphot - Radius
    #astro.teff_gspphot - Effective temperature
    #astro.mh_gspphot - Metallicity [Fe/H]
    #astro.mass_flame - Mass
    #astro.lum_flame - Luminosity
    #astro.evolstage_flame - Evolutionary stage (main sequence 100-360)
    #astro.spectraltype_esphs - Spectral type (to classify into mass ranges)
    #source.ruwe - (Renormalised unit weight error) Data quality

    query = """SELECT
        astro.source_id,
        astro.mass_flame,
        astro.mh_gspphot,
        astro.lum_flame,
        astro.evolstage_flame,
        astro.teff_gspphot,
        astro.radius_gspphot,
        astro.spectraltype_esphs,
        source.ruwe
    FROM gaiadr3.astrophysical_parameters as astro
    JOIN gaiadr3.gaia_source AS source
    USING (source_id)
    WHERE
        astro.mass_flame IS NOT NULL AND
        astro.mh_gspphot IS NOT NULL AND
        astro.lum_flame IS NOT NULL AND
        astro.spectraltype_esphs IS NOT NULL AND
        LOWER(astro.spectraltype_esphs) != 'unknown' AND
        astro.evolstage_flame BETWEEN 100 AND 360 AND
        source.ruwe <= 1.4
    """
    job = Gaia.launch_job_async(query)
    results = job.get_results()
    df = results.to_pandas()

    return df

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
    gaia_df = get_gaia()
    
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