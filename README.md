# Metrics Dashboard

A small plot.ly Dash app to view some of our internal metrics.


## Usage

1. Make sure your Google auth is set up: `gcloud auth application-default`
2. Set `GCLOUD_CREDS` to wherever those creds got saved to.
3. Set `CLOUD_SQL_CONNECTION_NAME` to the connection name found in [Google Cloud Console](https://console.cloud.google.com/sql/instances/).
4. Set `METRICS_DASHBOARD_DB_USERNAME`, `METRICS_DASHBOARD_DB_PASSWORD`, and `METRICS_DASHBOARD_DB_NAME` according to the secret in [Google Secret Manager](https://console.cloud.google.com/security/secret-manager/).
4. `docker compose up` and go to `localhost:8050`. use `dev`/`dev` to log in, unless you set your own custom `METRICS_DASHBOARD_USERNAME` and `METRICS_DASHBOARD_PASSWORD` env vars for some reason.


## Development


To get the Python environment working for your IDE completion etc.

1. Install `uv`
2. `uv sync`
3. configure your IDE to point at the virtualenv that `uv` created.

Then, to develop a new page, follow these steps.

**Note**: steps 2-3 are probably fastest done in a Jupyter notebook so you can get faster feedback loops on the visualization development. We have a Jupyter notebook in the docker-compose, so after `docker compose up` run `docker compose logs jupyter | grep token`, click that token-y link, and you'll be off to the races.

1. add a page to `pages/`: make a `layout` according to [the docs](https://dash.plotly.com/layout) and run `dash.register_page` according to [the other docs](https://dash.plotly.com/urls)
2. get your sql stuff set up:
    ```python
    from utils import get_sql

    engine, metadata = get_sql()

    # look in the pudl-usage-metrics repo's models.py for the db schema
    your_table = metadata.tables["your_table_name"]

    your_df = pd.read_sql(sa.select(...), engine)
    ```
3. use plot.ly express (`px`) to make a graph:
    ```python
    fig = px.histogram(...)
    ```
4. Shove that graph into the layout:
    ```python
    layout = html.Div(
        [
            ...
            dcc.Graph(id="your-cool-graph", figure=fig,
        ]
    )
    ```
