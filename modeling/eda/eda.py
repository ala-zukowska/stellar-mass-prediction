import os
import contextlib
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import zscore

def explore(df: pd.DataFrame, numerical_columns: list[str], categorical_columns: list[str], output_dir: str, hue_column: str | None = None) -> None:
    log_path = os.path.join(output_dir, f"eda_report.txt")

    with open(log_path, "w") as log_file:
        with contextlib.redirect_stdout(log_file):
            print(f"===== EDA Report: =====")
            describe_data(df[numerical_columns], df[categorical_columns])
            check_missing(df)
            identify_outliers(df[numerical_columns], os.path.join(output_dir, "outliers"))
            plot_single_distributions(df[numerical_columns], df[categorical_columns], os.path.join(output_dir, "single_distributions"))
            plot_relationships(df[numerical_columns + [hue_column]], output_dir, hue_column)
            check_coolineraity(df[numerical_columns], output_dir)
            print("\n")

def describe_data(df_numerical: pd.DataFrame, df_categorical: pd.DataFrame) -> None:
    print("\nSummary Statistics (Numerical Variables):\n")
    print(df_numerical.describe())
    print("\nSummary Statistics (Categorical Variables):\n")
    print(df_categorical.describe(include=["object", "category"]))

def check_missing(df: pd.DataFrame) -> None:
    print("\nMissing Values Analysis:\n")
    
    missing_df = df.isnull().sum()
    missing_df = missing_df[missing_df > 0].sort_values(ascending = False)
    
    print("Columns with missing values:")
    print(missing_df)

    missing_row_any = df.isnull().any(axis = 1).sum()
    missing_row_all = df.isnull().all(axis = 1).sum()
    no_missing_row = (~df.isnull().any(axis = 1)).sum()

    print("Rows with missing values:")
    print(f"Rows with at least one missing value: {missing_row_any}")
    print(f"Rows with all values missing: {missing_row_all}")
    print(f"Rows with no missing values: {no_missing_row}")

def identify_outliers(df: pd.DataFrame, output_dir: str, treshold: float = 3.0) -> None:
    print(f"\nZ-Score Based Outlier Detection (threshold = {treshold}):\n")
    
    z_scores = zscore(df, nan_policy="omit")
    z_df = pd.DataFrame(z_scores, columns=df.columns, index=df.index)

    for column in df.columns:
        print(f"Column: {column}")

        temp_df = pd.DataFrame({
            column: df[column],
            "Z-score": z_df[column]
        })
        outliers = temp_df[np.abs(temp_df["Z-score"]) > treshold]
        non_outliers = temp_df[np.abs(temp_df["Z-score"]) <= treshold]

        if outliers.empty:
            print("No outliers")
        else:
            print(outliers)

        plt.figure(figsize=(10,6))
        plt.scatter(non_outliers.index, non_outliers["Z-score"], label="Non-outliers", color="#0072B2", marker="o", s=25)
        plt.scatter(outliers.index, outliers["Z-score"], label="Outliers", color="#D55E00", marker="^", s=25)
        plt.title(f"Outliers Scatter Plot: {column}")
        plt.xlabel("Index")
        plt.ylabel("Z-score")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"outliers_{column}.png"))
        plt.show()

def plot_single_distributions(df_numerical: pd.DataFrame, df_categorical: pd.DataFrame, output_dir: str) -> None:
    for column in df_numerical.columns:
        ax = sns.histplot(df_numerical[column], bins=20, kde=True)
        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Count")
        plt.grid(True)
        ax.set_axisbelow(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"distribution_{column}.png"))
        plt.show()
    
    for column in df_categorical.columns:
        ax = sns.countplot(x=df_categorical[column])
        plt.title(f"Counts of {column}", pad=15)
        ax.bar_label(ax.containers[0], padding=3)
        ax.set_ylabel('')
        ax.yaxis.set_ticks([])
        ax.set_xlabel('')
        sns.despine(ax=ax, left=True, bottom=True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"categorical_{column}.png"))
        plt.show()

def plot_relationships(df: pd.DataFrame, output_dir: str, hue_column: str | None = None)  -> None:
    #Pairwise Relationships Between Variables
    wong_palette = ["#000000", "#e69f00", "#56b4e9", "#009e73", "#f0e442", "#0072b2", "#d55e00", "#cc79a7"]

    sns.pairplot(df, hue=hue_column, palette=wong_palette, plot_kws={'s': 10, 'alpha': 0.8})
    plt.suptitle(f"Pairwise Relationships", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"pairwise.png"))
    plt.show()

    #Multivariate Relationships
    fig = plt.figure(figsize=(12,10))

    plt.subplot(2, 2, 1)
    sns.scatterplot(data=df, x="L", y="M", hue=hue_column, palette=wong_palette)
    plt.title(f"Mass vs Luminosity")
    plt.legend('',frameon=False)

    plt.subplot(2, 2, 2)
    sns.scatterplot(data=df, x="Teff", y="L", hue=hue_column, palette=wong_palette)
    plt.gca().invert_xaxis()
    plt.title(f"Effective Temperature vs Luminosity (HR diagram)")
    plt.legend('',frameon=False)

    plt.subplot(2, 2, 3)
    sns.scatterplot(data=df, x="R", y="M", hue=hue_column, palette=wong_palette)
    plt.title(f"Radius vs Mass")
    plt.legend('',frameon=False)

    plt.subplot(2, 2, 4)
    sns.scatterplot(data=df, x="met", y="M", hue=hue_column, palette=wong_palette)
    plt.title(f"Metallicity vs Mass")
    plt.legend('',frameon=False)
    
    fig.subplots_adjust(hspace=0.3)
    handles, labels = plt.gca().get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=4)
    plt.savefig(os.path.join(output_dir, f"multivariate.png"))
    plt.show()

def check_coolineraity(df: pd.DataFrame, output_dir: str) -> None:
    correlation = df.corr()

    cmap = LinearSegmentedColormap.from_list("custom_blue_orange", ["#0072B2", "white", "#D55E00"])
    sns.heatmap(correlation, annot=True, cmap=cmap, fmt=".2f", vmin=-1, vmax=1)
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"collinearity.png"))
    plt.show()

def compare_distributions(df: pd.DataFrame, features: list[str], output_dir: str) -> None:
    df_melted = pd.DataFrame()

    for feature in features:
        df_temp = pd.melt(
            df,
            value_vars=[f"{feature}_nea", f"{feature}_gaia"],
            var_name="source",
            value_name="value"
        )
        df_temp["feature"] = feature
        df_temp["source"] = df_temp["source"].apply(lambda x: "NEA" if "nea" in x else "Gaia")
        df_melted = pd.concat([df_melted, df_temp], ignore_index=True)
    
    g = sns.FacetGrid(df_melted, col="feature", col_wrap=3, height=4, sharex=False, sharey=False)
    g.map_dataframe(
        sns.histplot,
        x="value",
        hue="source",
        kde=True,
        bins=30,
        palette= {"Gaia": "#0072B2","NEA": "#D55E00"},
        alpha=0.6
    ).add_legend()
    g.figure.subplots_adjust(top=0.9)
    g.figure.suptitle("NEA vs Gaia Feature Distributions", fontsize=16)
    plt.savefig(os.path.join(output_dir, f"compare_before_join.png"))
    plt.show()