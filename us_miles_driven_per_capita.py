import marimo

__generated_with = "0.8.0"
app = marimo.App(width="medium", app_title="US miles driven per capital")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import numpy as np

    import seaborn as sns
    sns.set_theme(style="darkgrid")
    import matplotlib.pyplot as plt
    return mo, np, pd, plt, sns


@app.cell
def __(mo):
    mo.md(
        """
        # A. Total miles driven each year in the US
        ## We'll need to pull data from 3 sources to get the maximum spread (1936 - 2023)

        - [1936 - 1995 PDF report](https://www.fhwa.dot.gov/ohim/summary95/vm201a.pdf). FIELD: "All Motor Vehicles => A. Total Travel"
        - "Report Archive 1992-2002" found on [this page under "archive"](https://www.fhwa.dot.gov/policyinformation/travel_monitoring/tvt.cfm). FIELD: "All Systems => Year"
        - (from the same FHWA page) 2000 - May 2024 by month is available if you download the `24maytvt.xlsx => subsheet: SAVMPT`. FIELD: we can simply aggregate `vmt` column by year, excluding 2024 which is not a complete year.

        ### NOTE: `vmt` ("vehicle miles traveled") is always in millions (so multiply by 1,000,000 to get actual value)
        """
    )
    return


@app.cell
def __(pd):
    # Ok, pasting in by hand the 1936 - 1995 report: https://www.fhwa.dot.gov/ohim/summary95/vm201a.pdf

    _years_36_95 = [year for year in range(1936, 1995 + 1)]
    # COLLAPSE ME:
    _values_total_travel_all_motor_vehicles_1936_1995 = [
    "252,128",
    "270,110",
    "271,177",
    "285,402",
    "302,188",
    "333,612",
    "268,224",
    "208,192",
    "212,713",
    "250,173",
    "340,880",
    "370,894",
    "397,957",
    "424,461",
    "458,246",
    "491,093",
    "513,581",
    "544,433",
    "561,963",
    "605,646",
    "631,161",
    "645,004",
    "664,653",
    "700,480",
    "718,762",
    "737,421",
    "766,734",
    "805,249",
    "846,298",
    "887,812",
    "925,899",
    "964,005",
    "1,015,869",
    "1,061,791",
    "1,109,724",
    "1,178,811",
    "1,259,786",
    "1,313,110",
    "1,280,544",
    "1,327,664",
    "1,402,380",
    "1,467,027",
    "1,544,704",
    "1,529,133",
    "1,527,295",
    "1,555,308",
    "1,595,010",
    "1,652,788",
    "1,720,269",
    "1,774,826",
    "1,834,872",
    "1,921,204",
    "2,025,962",
    "2,096,487",
    "2,144,362",
    "2,172,050",
    "2,247,151",
    "2,296,378",
    "2,357,588",
    "2,422,823"
    ]
    _rows = [[year, int(_values_total_travel_all_motor_vehicles_1936_1995[index].replace(',', ""))] for index, year in enumerate(_years_36_95)]

    by_year_1936_1995 = pd.DataFrame(_rows, columns=['year', 'vmt'])
    by_year_1936_1995
    return by_year_1936_1995,


@app.cell
def __(pd):
    # Hand copied here LOL
    _hand_copied = [
        # [1995, 2422819], # just to check overlap
        [1996,  2485846],
        [1997,  2560375],
        [1998,  2625367],
        [1999, 2691336],
        # [2000, 2746925] # check overlap
    ]
    by_year_1995_2000 = pd.DataFrame(_hand_copied, columns=['year', 'vmt'])
    return by_year_1995_2000,


@app.cell
def __(pd):
    by_month_2000_2024 = pd.read_csv(
        'data/Vehicle miles traveled 2000-May 2024 -- fhwa - 24maytvt > SAVMT.csv',
        thousands=','
    )

    by_month_2000_2024['year'] = by_month_2000_2024['obs_date'].apply(lambda x: '20' + x.split('-')[1])

    by_year_2000_2023 = by_month_2000_2024.groupby('year').agg({'vmt': 'sum'}).reset_index()

    by_year_2000_2023 = by_year_2000_2023[
            by_year_2000_2023['year'].apply(lambda x: int(x)) < 2024
    ]

    by_year_2000_2023
    return by_month_2000_2024, by_year_2000_2023


@app.cell
def __(
    by_year_1936_1995,
    by_year_1995_2000,
    by_year_2000_2023,
    pd,
    plt,
    sns,
):
    # Concat all 3 dataframes

    miles_driven_all_years = pd.concat([by_year_1936_1995, by_year_1995_2000, by_year_2000_2023])
    miles_driven_all_years['year'] = miles_driven_all_years.year.apply(lambda year: int(year))

    # make a time series chart using sns

    plt.figure(figsize=(12, 6))
    plt.figure(figsize=(16, 6))
    sns.lineplot(data=miles_driven_all_years, x='year', y='vmt')
    sns.lineplot(data=miles_driven_all_years, x='year', y='vmt')
    return miles_driven_all_years,


@app.cell
def __(mo):
    mo.md(
        r"""
        # B. US population by year (NOTE: population is in thousands, so multiply by 1,000)

        There's a lot of sources, not too many complete ones.

        [I used St Lous Fed](https://fred.stlouisfed.org/graph/?id=B230RC0A052NBEA,) to pull full 1936-2023 range.
        """
    )
    return


@app.cell
def __(pd):
    annual_population = pd.read_csv("data/us_annual_population_1936_2023.csv")
    annual_population['year'] = annual_population['date'].apply(lambda x: int(x.split('-')[0]))
    annual_population = annual_population[['year', 'population']]
    annual_population
    return annual_population,


@app.cell
def __(mo):
    mo.md(
        r"""
        # C. Gas prices (inflation adjusted)

        Solving this requires 2 things: 

        1. There are a lot of forms of gas (from crude to deisel). I want something close to "gas pump price" or "retail gas prices". I'm looking for as to close to the typical *consumer* pays as possible.
        2. There's no *single* source for 1930s-present, so I'll have to stitch together multiple.

        ### Data sources available

        - [1929-2015 "Average Historical Annual Gasoline Pump Price" excel spreadsheet](https://www.energy.gov/eere/vehicles/articles/fact-915-march-7-2016-average-historical-annual-gasoline-pump-price-1929): energy.gov published a fun little "fact" report, which weirdly seems to be the easiest place to cleanly get this big range of annual data.
        - [1994-2023 "U.S. All Grades All Formulations Retail Gasoline Prices"](https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=pet&s=emm_epm0_pte_nus_dpg&f=a): from the Energy Information Administration website. DOUBT: do we really want *all formulations* mushed together? I feel like that's not exactly "gasoline pump price", is it?
        - [1992 - 2023 "Regular conventional gasoline prices"](https://www.eia.gov/petroleum/gasdiesel/): comes straight from eia.gov data portal... so, better?
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"""### Import possible data sources""")
    return


@app.cell
def __(pd):
    gas_price_1929_2015 = pd.read_csv("data/US Average Annual Gasoline Pump Price, 1929 - 2015.csv")
    gas_price_1929_2015
    return gas_price_1929_2015,


@app.cell
def __(pd):
    gas_price_1994_2023 = pd.read_csv('data/U.S._All_Grades_All_Formulations_Retail_Gasoline_Prices.csv').rename(columns={"Year": "year"})
    gas_price_1994_2023
    return gas_price_1994_2023,


@app.cell
def __(pd):
    gas_prices_1992_2023 = pd.read_csv('data/Weekly U.S. Regular Conventional Retail Gasoline Prices  (Dollars per Gallon).csv')
    gas_prices_1992_2023

    gas_prices_1992_2023['year'] = gas_prices_1992_2023['Date'].apply(lambda x: int(x.split(', ')[1]))

    # aggregate on year
    gas_prices_1992_2023 = gas_prices_1992_2023.groupby('year').agg({'Weekly U.S. Regular Conventional Retail Gasoline Prices  (Dollars per Gallon)': 'mean'}).reset_index()

    gas_prices_1992_2023
    return gas_prices_1992_2023,


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Comparing the dataset we could use to extend to 2023, "Regular conventional retail" seems to differ least in the timeframe it overlaps with the 1929-2015... so, it's best? But... is it actually a good approximation? 

        At most, it seems off by 7 cents. I think this is accurate enough. Our chart's resolution and datasets variance means we're mostly just reacting to changes >20 cents, so this should be fine. I guess...
        """
    )
    return


@app.cell
def __(
    gas_price_1929_2015,
    gas_price_1994_2023,
    gas_prices_1992_2023,
    plt,
    sns,
):
    # merge all 3 gas price datasets on year (inner join, ie just keep where they all overlap)
    merged = gas_price_1929_2015.merge(
        gas_price_1994_2023,
        on="year",
        how="inner"
    ).merge(
        gas_prices_1992_2023,
        on="year",
        how="inner"
    )
    merged
    merged['a - b'] = merged['unajusted retail gas price'] - merged['All Grades All Formulations Retail Gasoline Price']
    merged['a - c'] = merged['unajusted retail gas price'] - merged['Weekly U.S. Regular Conventional Retail Gasoline Prices  (Dollars per Gallon)']

    merged['a - b'] = merged['a - b'].apply(lambda difference: abs(difference))
    merged['a - c'] = merged['a - c'].apply(lambda difference: abs(difference))

    # plot bot a - b and a - c columns next to each other, to see how they compare:
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=merged, x='year', y='a - b', label="a - b (ie 'All Grades All Formulations Retail'")
    sns.lineplot(data=merged, x='year', y='a - c', label="a - c, ie 'Weekly U.S. Regular Conventional Retail'")
    return merged,


@app.cell
def __(mo):
    mo.md(r"""### Create a unified gas price dataset, then adjust for inflation""")
    return


@app.cell
def __(gas_price_1929_2015, gas_prices_1992_2023, pd):
    gas_price_1929_2023 = pd.concat([
        gas_price_1929_2015,
        gas_prices_1992_2023[
            (gas_prices_1992_2023.year > 2015) &
            (gas_prices_1992_2023.year < 2024) # not a full year
        ].rename(columns={'Weekly U.S. Regular Conventional Retail Gasoline Prices  (Dollars per Gallon)': 'unajusted retail gas price'})
    ])

    gas_price_1929_2023.plot(x='year', y='unajusted retail gas price')
    return gas_price_1929_2023,


@app.cell
def __(gas_price_1929_2023):
    import cpi

    cpi.inflate(100, 1913)

    inflation_adjusted_gas_price = gas_price_1929_2023.copy().rename(columns={
        'unajusted retail gas price': 'raw gas price',
    })

    inflation_adjusted_gas_price['inflation adjusted gas price'] = inflation_adjusted_gas_price.apply(
        lambda row: cpi.inflate(round(row['raw gas price'], 2), int(row['year'])),
        axis=1
    )

    inflation_adjusted_gas_price.plot(x='year', y=['raw gas price', 'inflation adjusted gas price'])
    return cpi, inflation_adjusted_gas_price


@app.cell
def __(mo):
    mo.md(r"""# D. put it all into one cute lil' dataframe""")
    return


@app.cell
def __(
    annual_population,
    inflation_adjusted_gas_price,
    miles_driven_all_years,
):
    miles_driven_per_capita_and_gas_price = miles_driven_all_years.merge(
        annual_population,
        on="year",
        how="inner"
    ).merge(
        inflation_adjusted_gas_price,
        on="year",
        how="inner"
    )

    # NOTE: vmt is in millions, and popuation is in thousands, so to get actual value we can just multiply the quotient by 1,000
    miles_driven_per_capita_and_gas_price['miles driven per capita'] = 1000 * miles_driven_per_capita_and_gas_price['vmt'] / miles_driven_per_capita_and_gas_price['population']


    miles_driven_per_capita_and_gas_price
    return miles_driven_per_capita_and_gas_price,


@app.cell
def __(max_year, miles_driven_per_capita_and_gas_price, plt, sns):
    def draw_connected_scatter_plot(df, full_df):
        # Sort the dataframe by year
        df = df.sort_values(by="year")

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

        # Set the x-axis and y-axis limits
        plt.xlim(full_df["miles driven per capita"].min(), full_df["miles driven per capita"].max())
        plt.ylim(full_df["inflation adjusted gas price"].min(), full_df["inflation adjusted gas price"].max())

        # Annotate each point with the year
        for i in range(df.shape[0]):
            plt.text(
                df["miles driven per capita"].iloc[i],
                df["inflation adjusted gas price"].iloc[i],
                df["year"].iloc[i],
                fontsize=9,
                ha='right'
            )

        # Show the plot
        plt.xlabel("Miles Driven Per Capita")
        plt.ylabel("Inflation Adjusted Gas Price")
        plt.title("Scatter Plot of Miles Driven Per Capita vs Inflation Adjusted Gas Price")
        plt.show()

    draw_connected_scatter_plot(
        miles_driven_per_capita_and_gas_price[
            miles_driven_per_capita_and_gas_price.year <= max_year.value
        ], 
        miles_driven_per_capita_and_gas_price
    )
    return draw_connected_scatter_plot,


@app.cell
def __(miles_driven_per_capita_and_gas_price, mo):
    max_year = mo.ui.slider(
        start=miles_driven_per_capita_and_gas_price.year.min(),
        stop=miles_driven_per_capita_and_gas_price.year.max(),
    )

    max_year
    return max_year,


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
