import base64
import io
import dash
from dash import dcc, html, Input, Output, State, Dash, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from create_sankey_diagram import *
from functools import partial
import json
from mailtracker.app.get_dtpost_search import get_sendungsstatus



app = Dash(__name__) 

app.layout = html.Div(
    
    className='app-body', children=[
        html.Img(
        src='assets\logo.png',
        alt='Logo',
        style={'width':'160px',
                'position': 'fixed',
                'top': '2%',
                'right': '4.2%',
                }
            ),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag & Drop oder wähle eine ',
                html.A('Excel-Datei', style={'color': '#e63922'})
                ]),
            style={
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin-bottom': '9px',
            },
            multiple=True,
        ),
        html.Div(className='row', children=[
            html.Div(
                [html.Label('Spalten auswählen'),
                 dcc.Dropdown(
                    id='selection-source',
                    multi=True,
                    placeholder='Wähle die zu visualisierenden Spalten aus.',
                    value=[]
                ),
                 ],
                id='selection-source-container',
                className='twelve columns pretty_container'
            ),
        ]),
        html.Div(className='row', children=[
            html.Div(
                [html.Label(
                    f'Filtern nach'
                    ),
                dcc.Dropdown(
                    id=f'selection-target{count}',
                    multi=True,
                    placeholder='Wähle einen Wert',
                    value=[]
                ),
                ],
                id=f'selection-target-container{count}',
                className='two columns pretty_container'
            ) for count in range(7)
        ]),
        html.Div(
                [
                html.Button(
                    'Ansicht wechseln',
                    id='toggle-view',
                    style={
                        'color': '#e63922',
                        'margin': '10px'
                    }
                ),
                    
                html.Div(style={'flex': '1'}),
                
                     html.Button(
                    '1. Sendungsstatus abrufen',
                    id='mailtracker',
                    style={
                        'color': '#e63922',
                        'margin': '10px'
                    }
                ),
                    html.Button(
                    '2. Zu Excel exportieren',
                    id='download-button',
                    style={
                        'color': '#e63922',
                        'margin': '10px'
                    }
                )
                ],
                style={
                    'display': 'flex',
                    'align-items': 'center',
                    'width': '100%'
                }
        ),
        dcc.Download(id='download'),
        dcc.Graph(
        id='sankey',
        style={'height': '65vh'}
        ),
        dash_table.DataTable(
            id='table',
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
                },
            editable=True,
        ),
        dcc.Store(id='store'),
        dcc.Store(id='filename-store'),
        dcc.Store(id='selected-columns-store'),
#    
    
        # dbc.Button('Open modal', id='open', n_clicks=0),
        dbc.Modal(
            [
                # dbc.ModalHeader(
                    # dbc.ModalTitle(
                    #     'Excel-Datei heruntergeladen.',
                    #     style={
                    #         'font-weight': 'bold',
                    #         'text-align': 'center'
                    #         }
                    #     )
                    # ),
                html.Br(),
                dbc.ModalBody('Die Datei befindet sich in Downloads.'),
                html.Br(),
                dbc.ModalFooter(
                    dbc.Button(
                        'Schließen',
                        id='close',
                        className='ms-auto',
                        n_clicks=0,
                        style={
                            # 'text-align':'right',
                            'background-color':'#f2f2f2',
                            # 'border':'none'
                            }
                        )
                ),
            ],
            id='modal',
            is_open=False,
            style={
                'position': 'fixed',
                'top': '12%',
                'left': '50%',
                'transform': 'translate(-50%, -50%)',
                'width': '300px',
                'border-radius': '10px',
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                'background-color': 'white',
                'padding':'20px',
                'text-align':'center',
            },
        ),
    
#

        ]
    )

@app.callback(
    Output('store', 'data'),
    Output('filename-store', 'data'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')]
)
def upload_callback(contents, filename):
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        return df.to_json(
            date_format='iso',
            orient='split'),filename


@app.callback(
    Output('selection-source', 'options'),
    [Input('store', 'data')]
)
def available_options_changed_callback(data):
    df = pd.read_json(data, orient='split') if data else pd.DataFrame()
    available_columns = list(df.columns)
    opts = [{'label': opt, 'value': opt} for opt in available_columns]
    return opts

@app.callback(
    Output('selected-columns-store', 'data'),
    [Input('selection-source', 'value')]
)
def selected_columns_changed_callback(value):
    '''creates diagram only if at least two columns are selected'''
    return value

def show_target_options_changed_callback(index, style, data, selected_columns):
    df = pd.read_json(data, orient='split') if data else pd.DataFrame()
    if index >= len(selected_columns):
        return []
    column_values = df[selected_columns[index]].unique()
    opts = [{'label': opt, 'value': opt} for opt in column_values]
    return opts

for i in range(7):
    app.callback(
        Output(f'selection-target{i}', 'options'),
        [Input(f'selection-target-container{i}', 'style'),
        Input('store', 'data'),
        Input('selected-columns-store', 'data')]
    )(partial(show_target_options_changed_callback, i))

@app.callback(
    Output('sankey', 'figure'),
    [Input('store', 'data'),
     Input('filename-store', 'data'),
     Input('selected-columns-store', 'data')] +
    [Input(f'selection-target{i}', 'value') for i in range(7)]
)
def update_graph(data=None, filename=None, selected_columns = None, *filters):
    df = pd.read_json(data, orient='split') if data else pd.DataFrame()
    if filters == ([], [], [], [], [], [], []):
        filters = None
    if not selected_columns:
        try:
            selected_columns = list(df.columns)
        except Exception as e:
            print(e)

    title = 'Sankey Diagram'
    if not df.empty:
        title = filename
    fig = gen_sankey(
            df,
            selected_columns=selected_columns,
            filter=filters,
            linear=True,
            title=title
            )
    return fig

def parse_data(contents, filename):
    content_string = contents.split(',')[1]
    decoded = base64.b64decode(content_string)
    try:
        if "xlsx" in filename:
            df = pd.read_excel(io.BytesIO(decoded))
            # df['Review'] = 'unknown'
            # df['Comment'] = 'no comment'
            df.name = filename
            return df
    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])

@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    [Input('store', 'data'),
     Input('selected-columns-store', 'data')]
)
def update_table(data, selected_columns):
    if not selected_columns:
        data_cols = json.loads(data)
        data_cols = list(data_cols['columns'])
        data_cols = data_cols[:-2]
        try:
            selected_columns = data_cols
        except Exception as e:
            print(e)
    df = pd.read_json(data, orient='split')
    df = df[selected_columns]
    columns = [{'name': i, 'id': i} for i in df.columns]
    return df.to_dict('records'), columns

@app.callback(
    [Output('download-button', 'n_clicks'),
     Output('modal', 'is_open')],
    [Input('download-button', 'n_clicks'),
     Input('close', 'n_clicks')],
    [State('modal', 'is_open')]
)
def on_button_click_and_toggle_modal(n_clicks, close_clicks, is_open):
    if n_clicks is None:
        raise PreventUpdate

    # Wenn der Download-Button geklickt wurde, öffnet sich das Modal
    if n_clicks > 0 and not is_open:
        get_sendungsstatus()
        return n_clicks, True

    # Wenn der Close-Button geklickt wurde, schließt sich das Modal
    if close_clicks:
        return dash.no_update, False

    return n_clicks, is_open

# @app.callback(
#     Output('download-button', 'n_clicks'),
#     Input('download-button', 'n_clicks')
# )

# def on_button_click(n_clicks):
#     if n_clicks is None:
#         raise PreventUpdate
#     else:
#         get_sendungsstatus()
#         return n_clicks

# @app.callback(
#     Output("modal", "is_open"),
#     [Input("open", "n_clicks"), Input("close", "n_clicks")],
#     [State("modal", "is_open")],
# )
# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open

application = app.server

if __name__ == '__main__':
    application.run(
        debug=False,
        host = '0.0.0.0',
        port='8050'
    )
