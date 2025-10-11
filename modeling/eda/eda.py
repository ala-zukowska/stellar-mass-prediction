import os
import contextlib
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import zscore
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def explore(df: pd.DataFrame, numerical_columns: list[str], categorical_columns: list[str], output_dir: str, hue_column: str | None = None) -> None:
    log_path = os.path.join(output_dir, f"eda_report.txt")

    with open(log_path, "w") as log_file:
        with contextlib.redirect_stdout(log_file):
            print(f"===== EDA Report: =====")
            describe_data(df[numerical_columns], df[categorical_columns])
            check_missing(df)
            identify_outliers(df[numerical_columns], os.path.join(output_dir, "outliers"))
            plot_single_distributions(df[numerical_columns], df[categorical_columns], os.path.join(output_dir, "single_distributions"))
            plot_pairwise_relationships(df[numerical_columns + [hue_column]], output_dir, hue_column)
            plot_multivariate(df, df[numerical_columns], output_dir, hue_column)
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

def plot_pairwise_relationships(df: pd.DataFrame, output_dir: str, hue_column: str | None = None) -> None:
    palette = _get_colors(df[hue_column].dropna().unique())

    sns.pairplot(df, hue=hue_column, palette=palette, plot_kws={'s': 10, 'alpha': 0.8})
    plt.suptitle(f"Pairwise Relationships", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"pairplot.png"))
    plt.show()


    fig = plt.figure(figsize=(12,10))

    ax = plt.subplot(2, 2, 1)
    sns.scatterplot(data=df, x="L", y="M", hue=hue_column, palette=palette, ax=ax)
    sns.regplot(data=df, x="L", y="M", scatter=False, line_kws={'color': "#d55e00", 'linewidth': 1.5}, ax=ax, ci=None)
    plt.title(f"Mass vs Luminosity")
    plt.legend('',frameon=False)

    ax = plt.subplot(2, 2, 2)
    sns.scatterplot(data=df, x="Teff", y="L", hue=hue_column, palette=palette, ax=ax)
    sns.regplot(data=df, x="Teff", y="L", scatter=False, line_kws={'color': "#d55e00", 'linewidth': 1.5}, ax=ax, ci=None)
    plt.gca().invert_xaxis()
    plt.title(f"Effective Temperature vs Luminosity (HR diagram)")
    plt.legend('',frameon=False)

    ax = plt.subplot(2, 2, 3)
    sns.scatterplot(data=df, x="R", y="M", hue=hue_column, palette=palette, ax=ax)
    sns.regplot(data=df, x="R", y="M", scatter=False, line_kws={'color': "#d55e00", 'linewidth': 1.5}, ax=ax, ci=None)
    plt.title(f"Radius vs Mass")
    plt.legend('',frameon=False)

    ax = plt.subplot(2, 2, 4)
    sns.scatterplot(data=df, x="met", y="M", hue=hue_column, palette=palette, ax=ax)
    for i, spectype in enumerate(df[hue_column].dropna().unique()):
        subset = df[df[hue_column] == spectype]
        sns.regplot(data=subset, x="met", y="M", scatter=False, line_kws={'color': palette[i % len(palette)], 'linewidth': 1.5}, ax=ax, ci=None)
    plt.title(f"Metallicity vs Mass")
    plt.legend('',frameon=False)
    
    fig.subplots_adjust(hspace=0.3)
    handles, labels = plt.gca().get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=4)
    plt.savefig(os.path.join(output_dir, f"pairwise_with_regression.png"))
    plt.show()

def plot_multivariate(df: pd.DataFrame, df_numerical: pd.DataFrame, output_dir: str, hue_column: str | None = None) -> None:
    _plot_3d_scatter(df, ["Teff", "L", "M"], output_dir, hue_column)
    _plot_3d_scatter(df, ["L", "M", "met"], output_dir, hue_column, 2)
    _plot_pca_projection(df, df_numerical, output_dir, hue_column)

def _plot_3d_scatter(df: pd.DataFrame, list_xyz: list[str], output_dir: str, hue_column: str | None = None, file_suffix: int = 1) -> None:
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    if hue_column:
        categories= df[hue_column].dropna().unique()
        palette = _get_colors(categories)
    
    for i, category in enumerate(categories):
        subset = df[df[hue_column] == category]
        ax.scatter(
            subset[list_xyz[0]],
            subset[list_xyz[1]],
            subset[list_xyz[2]],
            label=category,
            color=palette[i],
            s=30,
            alpha=0.7
        )
    
    ax.set_xlabel(f"{list_xyz[0]}")
    ax.set_ylabel(f"{list_xyz[1]}")
    ax.set_zlabel(f"{list_xyz[2]}")
    ax.set_title(f"{list_xyz[0]} vs {list_xyz[1]} vs {list_xyz[2]} Colored by {hue_column}")
    ax.legend(title=hue_column, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"3d_scatter_plot_{file_suffix}.png"))
    plt.show()

def _plot_pca_projection(df: pd.DataFrame, df_numerical: pd.DataFrame, output_dir: str, hue_column: str | None = None) -> None:
    print(f"\nPCA Explained Variance:\n")
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(df_numerical)

    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(data_scaled)
    pc_df = pd.DataFrame(data=principal_components, columns=["PC1", "PC2"], index=df_numerical.index)

    pca_loadings = pd.DataFrame(pca.components_.T, index=df_numerical.columns, columns=['PC1', 'PC2'])

    print(f"PC1: {pca.explained_variance_ratio_[0]}")
    print(f"PC2: {pca.explained_variance_ratio_[1]}")
    print("PCA Loadings:\n", pca_loadings)

    if hue_column:
        pc_df[hue_column] = df[hue_column]
        palette = _get_colors(df[hue_column].dropna().unique())
    
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=pc_df, x="PC1", y="PC2", hue=hue_column, palette=palette, alpha=0.7, s=40)
    plt.title("PCA Projection (2D)", fontsize=14)
    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "pca_projection.png"))
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

def _get_colors(categories: list[str]):
    wong_palette = ["#000000", "#e69f00", "#56b4e9", "#009e73", "#f0e442", "#0072b2", "#d55e00", "#cc79a7"]
    needed = len(categories)
    return wong_palette[:needed]