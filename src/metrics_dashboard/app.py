import os

import dash
import dash_auth
from dash import Dash, html, dcc


BASIC_AUTH = {
    os.environ["METRICS_DASHBOARD_USERNAME"]: os.environ["METRICS_DASHBOARD_PASSWORD"]
}

app = Dash(__name__, use_pages=True)
app.server.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

# TODO 2025-03-06 one day we could use dash_auth.OIDCAuth but basic works for now.
auth = dash_auth.BasicAuth(app, BASIC_AUTH)

app.layout = html.Div(
    [
        html.H1("Multi-page app with Dash Pages"),
        html.Div(
            [
                html.Div(
                    dcc.Link(
                        f"{page['name']} - {page['path']}", href=page["relative_path"]
                    )
                )
                for page in dash.page_registry.values()
            ]
        ),
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
