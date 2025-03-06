from datetime import datetime, timedelta
import dash
import pandas as pd
import plotly.express as px
import sqlalchemy as sa
from dash import html, dcc

from metrics_dashboard.utils import get_sql

dash.register_page(__name__)

engine, metadata = get_sql()

s3_logs = metadata.tables["out_s3_logs"]

logs_df = pd.read_sql(
    sa.select(s3_logs.c.time, s3_logs.c.table).where(
        s3_logs.c.time > datetime.now() - timedelta(weeks=2)
    ),
    engine,
)

fig = px.histogram(data_frame=logs_df, color="table", x="time")


layout = html.Div(
    [
        html.H1("Last 2 weeks S3 downloads"),
        html.Br(),
        dcc.Graph(id="last-2-weeks-s3-downloads", figure=fig),
    ]
)
