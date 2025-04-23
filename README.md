# energy-data
 General collection and processing of energy related data: oil, consumption, etc

# Developer notes

## David's workflow
1. Using virtualenvwrapper (which has all my installations): `workon data_work`
2. I'm hip, so I spurn jupyter in favor of marimo: `marimo edit FILE_NAME.py` or just `marimo edit` to create
3. Raw, external data sources in `data/`, outputs I create go in `data/derived-data`