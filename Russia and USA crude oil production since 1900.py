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
def __(np, pd, raw_df, sns):
    df = raw_df.rename(columns={"Year": "year", "oil_production__twh": "oil_production_twh", "Entity": "country"})

    # Rename country between certain regions: 
    # "USSR" 1900 - USSR_START should be "Russian Empire" (note it's inclusive, because we want the line to be continuous visually)
    USSR_START = 1922
    df['country'] = np.where(
        (df['country'] == 'USSR') & (df['year'] <= USSR_START), 
        'Russian Empire', 
        df['country']
    )
    # Manually duplicate 'Russian Empire' for the years 1922 and rename it USSR:
    df = pd.concat([
        df,
        df[
            (df['country'] == 'Russian Empire') & 
            (df['year'] == USSR_START)
        ].assign(year=USSR_START, country='USSR')
    ])


    # "USSR" should only exist USSR_START - USSR_END, anything "USSR" after should be dropped
    USSR_END = 1991
    df = df[~((df['country'] == 'USSR') & (df['year'] > USSR_END))]
    # "Russia" should only exist USSR_END - present, anything before USSR_END should be dropped
    df = df[~((df['country'] == 'Russia') & (df['year'] < USSR_END))]


    sns.lineplot(data=df, x="year", y="oil_production_twh", hue="country")
    return USSR_END, USSR_START, df


@app.cell
def __(df):
    # Sort the data by year
    sorted_df = df.sort_values(by="year")

    # Create dictionary with data for each country
    output_dict = {
        country: sorted_df[sorted_df['country'] == country].to_dict('records')
        for country in sorted_df['country'].unique()
    }

    # Convert to JSON format, print to a file
    import json
    json_output = json.dumps(output_dict, indent=2)
    return json, json_output, output_dict, sorted_df


@app.cell
def __(mo):
    mo.md(r"""# Copy json output to clipboard for export""")
    return


@app.cell
def __(json_output):
    import pyperclip
    pyperclip.copy(json_output)
    return (pyperclip,)


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
