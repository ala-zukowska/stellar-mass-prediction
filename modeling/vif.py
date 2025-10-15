import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.api import add_constant
from pathlib import Path

dir = Path(__file__).resolve().parent
df = add_constant(pd.read_csv(dir / "preprocessor/output/joined_out.csv")[["L", "met"]])

vif_df = pd.DataFrame()
vif_df["Pred"] = ["intercept", "L", "met"]
vif_df['VIF'] = [variance_inflation_factor(df, i) for i in range(df.shape[1])]

print(vif_df)   # ~1