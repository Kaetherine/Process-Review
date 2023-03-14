import base64
import io
import dash
from dash import dcc, html, Input, Output, Dash
import plotly.graph_objs as go
from controller import *

df = {}
available_cols = []
selected_cols = []
app = Dash(__name__)

app.layout = html.Div(className='app-body', children=[
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=True,
        ),
        html.Div(className="row", children=[
            html.Div(
                [html.Label('Select source columns'),
                 dcc.Checklist(
                     id='selection-source',
                     options=[{'label': opt, 'value': opt} for opt in available_cols],
                     value=[]
                 ),
                 ],
                id='selection-source-container',
                style=dict(display='none'),
                className="four columns pretty_container"
            ),
            html.Div(
                [html.Label('Select target column'),
                 dcc.RadioItems(
                     id='selection-target',
                     options=[{'label': opt, 'value': opt} for opt in available_cols],
                     value=''
                 ),
                 ],
                id='selection-target-container',
                style=dict(display='none'),
                className="four columns pretty_container"
            ),
        ]),
        html.Button('Submit', id='submit', n_clicks=0, style=dict(display='none')),
        dcc.Graph(id="sankey")
    ]
)


@app.callback(
    Output("selection-source-container", "style"),
    [Input("upload-data", "contents"),
     Input("upload-data", "filename")]
)
def upload_callback(contents, filename):
    global df
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        show = len(df) > 2
        if show:
            return dict()
    return dict(display='none')


@app.callback(
    Output("selection-source", "options"),
    [Input("selection-source-container", "style")]
)
def available_options_changed_callback(style):
    opts = []
    if 'display' in style.keys():
        return opts
    available_cols = list(df.columns)
    print(available_cols)
    opts = [{'label': opt, 'value': opt} for opt in available_cols]
    return opts


@app.callback(
    Output("selection-target-container", "style"),
    [Input("selection-source", "value")]
)
def selected_cols_changed_callback(value):
    #global selected_cols
    #selected_cols = value
    #print(selected_cols)
    show = len(value) > 1
    if show:
        return dict()
    return dict(display='none')


@app.callback(
    Output("selection-target", "options"),
    [Input("selection-target-container", "style")]
)
def show_target_options_changed_callback(style):
    opts = []
    if 'display' in style.keys():
        return opts
    available_cols = list(df.columns)
    print(available_cols)
    opts = [{'label': opt, 'value': opt} for opt in available_cols]
    return opts


@app.callback(
    Output("submit", "style"),
    [Input("selection-target", "value")]
)
def select_all_none(value):
    show = len(value) == 1
    if show:
        return dict()
    return dict(display='none')


@app.callback(
    Output('sankey', 'figure'),
    [Input("selection-source", "value"), Input("selection-target", "value")]
)
def update_graph(source, target):
    global df
    cols_selcted = len(source)
    if 1 < cols_selcted < 6 and target != '':
        fig = gen_sankey(df, cols=source, value_cols=target)
        return fig
    fig = go.Figure()
    return fig


def parse_data(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    try:
        if "xlsx" in filename:
            return pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])
    return None


def extract_df():
    new_df = df[selected_cols].copy()
    return new_df


if __name__ == '__main__':
    app.run_server(debug=True)
