import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore
import mpld3
from mpld3 import plugins
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from scipy.stats import linregress

def create_graphs(df: pd.DataFrame, numerical_columns: list[str], categorical_columns: list[str], output_dir: str, hue_column: str | None = None) -> None:
    _identify_outliers_mpld3(df[numerical_columns], output_dir)
    _plot_categorical_plotly(df[categorical_columns], output_dir)
    _plot_pairwise_plotly(df[numerical_columns + [hue_column]], output_dir, hue_column)
    _plot_3d_scatter_plotly(df, ["Teff", "L", "M"], output_dir, hue_column, 1, dict(x=-1.25, y=1.25, z=0.8))
    _plot_3d_scatter_plotly(df, ["L", "M", "met"], output_dir, hue_column, 2, dict(x=1.25, y=-1.25, z=0.8))
    _check_coolinearity_plotly(df[numerical_columns], output_dir)

def _identify_outliers_mpld3(df: pd.DataFrame, output_dir: str, treshold: float = 3.0) -> None:
    z_scores = zscore(df, nan_policy="omit")
    z_df = pd.DataFrame(z_scores, columns=df.columns, index=df.index)

    for column in df.columns:
        if column == "M":
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
            plt.title(f"Outliers Scatter Plot: {column}", fontsize=20)
            plt.xlabel("Index", fontsize=16)
            plt.ylabel("Z-score", fontsize=16)
            plt.legend(fontsize=14)
            plt.xticks(fontsize=14)
            plt.yticks(fontsize=14)
            plt.grid(True)
            plt.tight_layout()
        
            # plugins.connect(plt.gcf(), plugins.MousePosition())
            # with open(os.path.join(output_dir, f"outliers_{column}.html"), "w") as f:
            #     f.write(mpld3.fig_to_html(plt.gcf()))
            plt.close()

def _plot_categorical_plotly(df_categorical: pd.DataFrame, output_dir: str) -> None:
    order = ["A", "F", "G", "K", "M"]
    
    for column in df_categorical.columns:
        fig = px.histogram(
            df_categorical,
            x=column,
            title=f"Counts of {column}",
            text_auto=True,
            color=column,
            category_orders={column: order},
            color_discrete_sequence=_get_colors(order)

        )
        fig.update_layout(
            xaxis_title='',
            yaxis_title='',
            title_x=0.5,
            yaxis=dict(showticklabels=False),
            xaxis=dict(showticklabels=True),
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='white',
            width=750,
            height=600
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        fig.write_html(os.path.join(output_dir, f"categorical_{column}.html"))

def _plot_pairwise_plotly(df: pd.DataFrame, output_dir: str, hue_column: str | None = None) -> None:
    spectype_order = ["A", "F", "G", "K", "M"]
    unique_types = [st for st in spectype_order if st in df[hue_column].dropna().unique()] if hue_column else []

    palette = _get_colors(unique_types)
    plots = [
        {"x": "L", "y": "M", "title": "Mass vs Luminosity", "reverse_x": False},
        {"x": "Teff", "y": "L", "title": "Effective Temperature vs Luminosity (HR diagram)", "reverse_x": True},
        {"x": "R", "y": "M", "title": "Radius vs Mass", "reverse_x": False},
        {"x": "met", "y": "M", "title": "Metallicity vs Mass", "reverse_x": False}
    ]

    fig = make_subplots(rows=2, cols=2, subplot_titles=[p["title"] for p in plots], vertical_spacing=0.1)
    for idx, plot in enumerate(plots):
        row = idx // 2 + 1
        col = idx % 2 + 1
        x_data = df[plot["x"]]
        y_data = df[plot["y"]]

        for i, spectype in enumerate(unique_types):
            subset = df[df[hue_column] == spectype]
            fig.add_trace(go.Scatter(
                x=subset[plot["x"]], 
                y=subset[plot["y"]],
                mode='markers',
                marker=dict(size=4, color=palette[i % len(palette)]),
                name=spectype,
                showlegend=(row == 1 and col == 1)
                ), row=row, col=col)

        if plot["x"] == "met":
            for i, spectype in enumerate(unique_types):
                subset = df[df[hue_column] == spectype]
                slope, intercept, _, _, _ = linregress(subset[plot["x"]], subset[plot["y"]])
                fig.add_trace(go.Scatter(
                    x=np.sort(subset[plot["x"]]),
                    y=intercept + slope * np.sort(subset[plot["x"]]),
                    mode='lines',
                    line=dict(color=palette[i % len(palette)], width=2),
                    showlegend=False
                ), row=row, col=col)
        else:
            slope, intercept, _, _, _ = linregress(x_data, y_data)
            fig.add_trace(go.Scatter(
                x=np.sort(x_data),
                y=intercept + slope * np.sort(x_data),
                mode='lines',
                line=dict(color='#d55e00', width=2),
                showlegend=False
            ), row=row, col=col)
        
        if plot.get("reverse_x", False):
            fig.update_xaxes(autorange="reversed", row=row, col=col)
        
    fig.update_layout(
        width=1000,
        height=800,
        title_text="Pairwise Plots with Regression Lines",
        title_x=0.5
    )

    fig.write_html(os.path.join(output_dir, f"pairwise.html"))

def _plot_3d_scatter_plotly(df: pd.DataFrame, list_xyz: list[str], output_dir: str, hue_column: str | None = None, file_suffix: int = 1, camera: dict = dict(x=1.25, y=1.25, z=1.25)) -> None:
    if hue_column:
        spectype_order = ["A", "F", "G", "K", "M"]
        categories = [st for st in spectype_order if st in df[hue_column].dropna().unique()]
        palette = _get_colors(categories)
        color_discrete_map = {category: palette[i] for i, category in enumerate(categories)}
    
    fig = px.scatter_3d(
        df, 
        x=list_xyz[0], 
        y=list_xyz[1], 
        z=list_xyz[2], 
        color=hue_column, 
        category_orders = {hue_column: categories},
        color_discrete_map=color_discrete_map, 
        opacity=0.85
    )
    fig.update_traces(marker = dict(size = 3.5)) 
    fig.update_layout(scene_camera = dict(eye = camera))

    fig.write_html(os.path.join(output_dir, f"3d_scatter_plot_{file_suffix}.html"))

def _check_coolinearity_plotly(df: pd.DataFrame, output_dir: str) -> None:
    fig = px.imshow(
        df.corr(),
        text_auto=".2f",
        color_continuous_scale=[(0.0, "#0072B2"), (0.5, "white"), (1.0, "#D55E00")],
        zmin=-1,
        zmax=1
    )
    fig.update_layout(
        title="Correlation Matrix",
        title_x=0.5,
        xaxis_title="",
        yaxis_title="",
        font=dict(size=16),
        coloraxis_colorbar=dict(x=1.05, y=0.5),
        width=750,
        height=600 
    )

    fig.write_html(os.path.join(output_dir, "collinearity.html"))

def compare_distributions_plotly(df: pd.DataFrame, features: list[str], output_dir: str) -> None:
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
    
    fig = make_subplots(rows=2, cols=3, subplot_titles=features, vertical_spacing=0.1)

    for i, feature in enumerate(features):
        row = i // 3 + 1
        col = i % 3 + 1
        df_feat = df_melted[df_melted["feature"] == feature]

        fig.add_trace(go.Histogram(
                x=df_feat[df_feat["source"] == "Gaia"]["value"],
                name="Gaia",
                opacity=0.6,
                marker_color="#0072B2",
                nbinsx=100,
                showlegend=(i==0)
                ), row=row, col=col)
        
        fig.add_trace(go.Histogram(
                x=df_feat[df_feat["source"] == "NEA"]["value"],
                name="NEA",
                opacity=0.6,
                marker_color="#D55E00",
                nbinsx=100,
                showlegend=(i==0)
                ), row=row, col=col)
        
    fig.update_layout(
        title_text="NEA vs Gaia Feature Distributions",
        title_x=0.5,
        title_font_size=20,
        barmode='overlay',
        legend=dict(title="Source", font=dict(size=14)),
        height=800,
        width=1200
    )

    fig.write_html(os.path.join(output_dir, "compare_before_join.html"))

def _get_colors(categories: list[str]):
    wong_palette = ["#f0e442", "#000000", "#56b4e9", "#e69f00", "#009e73", "#0072b2", "#d55e00", "#cc79a7"]
    needed = len(categories)
    return wong_palette[:needed]