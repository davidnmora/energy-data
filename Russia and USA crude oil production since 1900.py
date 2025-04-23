import marimo

__generated_with = "0.9.23"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    return mo, np, pd, plt, sns


@app.cell
def __():
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        # Import data

        From [Our World in Data](https://ourworldindata.org/grapher/oil-production-by-country?country=USA~OWID_USS~RUS) API
        """
    )
    return


@app.cell
def __(pd):
    raw_df= pd.read_csv(
        "https://ourworldindata.org/grapher/oil-production-by-country.csv?v=1&csvType=filtered&useColumnShortNames=true&country=USA~OWID_USS~RUS", 
        storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'}
    ).drop(columns='Code')
    return (raw_df,)


@app.cell
def __(raw_df):
    raw_df
    return


@app.cell
def __(raw_df, sns):
    # Plot the a line for each of the 3 Code column unique entities:
    # 1. USA
    # 2. OWID_USS
    # 3. RUS
    # Plot the data

    sns.lineplot(data=raw_df, x="Year", y="oil_production__twh", hue="Entity")
    return


@app.cell
def __(mo):
    mo.md(r"""# Edit and format the data""")
    return


@app.cell
def __(np, raw_df, sns):
    df = raw_df.rename(columns={"Year": "year", "oil_production__twh": "oil_production_twh", "Entity": "country"})

    # Rename country between certain regions: 
    # "USSR" 1900 - 1921 should be "Russian Empire"
    df['country'] = np.where(
        (df['country'] == 'USSR') & (df['year'] < 1922), 
        'Russian Empire', 
        df['country']
    )
    # "USSR" should only exist 1922 - 1991, anything "USSR" after should be dropped
    df = df[~((df['country'] == 'USSR') & (df['year'] > 1991))]
    # "Russia" should only exist 1991 - present, anything before 1991 should be dropped
    df = df[~((df['country'] == 'Russia') & (df['year'] < 1991))]


    sns.lineplot(data=df, x="year", y="oil_production_twh", hue="country")
    return (df,)


@app.cell
def __(df):
    # Sort the data by year
    sorted_df = df.sort_values(by="year")
    """
    I want to output a JSON in the format
    {
        usa: [] # all the usa data,
        russianEmpire: [...],
        ussr: [...],
        russia: [...]
    }
    """

    return (sorted_df,)


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
