import marimo

__generated_with = "0.8.0"
app = marimo.App(width="medium", app_title="Gas price roller coaster")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import numpy as np

    import functools

    import seaborn as sns
    sns.set_theme(style="darkgrid")
    import matplotlib.pyplot as plt
    return functools, mo, np, pd, plt, sns


@app.cell
def __(mo):
    mo.md(
        r"""
        # How has average miles driven per capita varied alongside retail gasoline price in the US?

        Inspired by this 2010 NYTimes connected scatter plot, *[Driving Shifts into Reverse](https://archive.nytimes.com/www.nytimes.com/imagepages/2010/05/02/business/02metrics.html)*.
        """
    )
    return


@app.cell
def __(pd):
    miles_driven_per_capita_and_gas_price = pd.read_csv('data/derived-data/miles_driven_per_capita_and_gas_price.csv')
    return miles_driven_per_capita_and_gas_price,


@app.cell
def __(miles_driven_per_capita_and_gas_price, mo):
    max_year = mo.ui.range_slider.from_series(miles_driven_per_capita_and_gas_price.year, full_width=True)

    mo.md(
        f"""
        # Filter within the time range: 1936 - 2023
        {max_year}
        """
    )
    return max_year,


@app.cell
def __(
    functools,
    max_year,
    miles_driven_per_capita_and_gas_price,
    plt,
    sns,
    xlim,
    ylim,
):
    def format_year(year):
        return "'" + f'{year}'[-2:]

    @functools.cache
    def draw_connected_scatter_plot(min, max):
        full_df = miles_driven_per_capita_and_gas_price
        df = miles_driven_per_capita_and_gas_price[
            (miles_driven_per_capita_and_gas_price.year <= max) &
            (miles_driven_per_capita_and_gas_price.year >= min)
        ]

        # Create the scatter plot
        plt.figure(figsize=(10, 6))
        scatter_plot = sns.scatterplot(
            data=df,
            x="miles driven per capita",
            y="inflation adjusted gas price"
        )

        # Add lines connecting the points
        plt.plot(
            df["miles driven per capita"],
            df["inflation adjusted gas price"],
            linestyle='-', 
            marker='o'
        )

        # Set the x-axis and y-axis limits.
        plt.xlim(*xlim)
        plt.ylim(*ylim)

        # Annotate each point with the year
        for i in range(df.shape[0]):
            plt.text(
                df["miles driven per capita"].iloc[i],
                df["inflation adjusted gas price"].iloc[i],
                format_year(df["year"].iloc[i]),
                fontsize=9,
                ha='right'
            )

        # Show the plot
        plt.xlabel("Miles Driven Per Capita")
        plt.ylabel("Inflation Adjusted Gas Price (USD)")
        plt.title("Scatter Plot of Miles Driven Per Capita vs Inflation Adjusted Gas Price")
        return plt.gca()


    draw_connected_scatter_plot(max_year.value[0], max_year.value[1])
    return draw_connected_scatter_plot, format_year


@app.cell
def __():
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()