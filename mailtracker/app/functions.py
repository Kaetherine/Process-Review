import requests
import pandas as pd

def generate_sankey_diagram(df, selected_columns=None, filter=None,
                    linear=True, title='Sankey Diagram'):
    '''create the sankey diagram based on given params'''
    
    df = df.copy()

    if selected_columns == list(df.columns):
        selected_columns = selected_columns[:-1]
    else:
        selected_columns.append(selected_columns[-1])

    if filter != None:
        for i in range(len(filter)-1):
            if filter[i] == []:
                continue
            df = df.loc[df[selected_columns[i]].isin(filter[i])]
 
    if linear:
        for col in list(df.columns):
            for index, value in df[col].items():
                if str(col) not in str(value):
                    df.loc[index, col] = f'{value} ({col})'

    df['count_col'] = [f'count_{x}' for x in range(len(df))]


    # Create a list of dataframes with source and target columns
    dfs = []
    for column in selected_columns:
        i = selected_columns.index(column)+1
        if (column == selected_columns[-1] or
            column == selected_columns[-2] or
            column == 'count_col'
            ):
            continue
        else:
            try:
                dfx = df.groupby([column, selected_columns[i]])
                dfx = dfx['count_col'].count().reset_index()
                dfx.columns = ['source', 'target', 'count']
                dfs.append(dfx)
            except Exception as e:
                print(f'columnname: {column}\n{repr(e)}')

    # Concatenate dataframes
    links = pd.concat(dfs, axis=0)
    unique_source_target = list(
        pd.unique(links[['source', 'target']].values.ravel('K'))
        )
    mapping_dict = {k: v for v, k in enumerate(unique_source_target)}
    links['source'] = links['source'].map(mapping_dict)
    links['target'] = links['target'].map(mapping_dict)
    links_dict = links.to_dict(orient='list')

    # Define sankey diagram nodes and links
    data = dict(
        type='sankey',
        node=dict(
            pad=15,
            thickness=20,
            line=dict(
                color='#e63922',
                width=0.1
            ),
            label=unique_source_target,
            color='#e63922'
        ),
        link=dict(
            source=links_dict['source'],
            target=links_dict['target'],
            value=links_dict['count']
        )
    )

    # Define layout
    layout = dict(
    title=title,
    font=dict(
        size=16
    )
    )
    # Create sankey diagram
    fig = dict(data=[data], layout=layout)
    
    return fig

# mail_ids = [
#         'A005BCE237000000003E',
#         'A005BCE2370000000047',
#         ]

def get_mail_status(mail_ids):
    url = "https://www.deutschepost.de/int-verfolgen/data/search"
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "referer": "https://www.deutschepost.de/de/s/sendungsverfolgung.html",
        }
    cookies = {
        "verfolgenSL": "eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiZGlyIn0..-R6mTuXgyZcvLd4X32eEMw...",
        "_abck": "6280D482FE82DB5DE5656B88A63F313D~0~YAAQlKAkFwlgx9WSAQAAaGHW4QwxrrC...",
        "bm_sv": "8C9E8E77137677EB5555599BA65BC2A6~YAAQlKAkFztpx9WSAQAAVJ/W4RmDX45e...",
        }

    for mail_id in mail_ids:
        params = {
            'piececode': mail_id,
            'inputSearch': 'true',
            'language': 'de'
        }
        try:
            response = requests.get(
                url=url,
                headers=headers,
                cookies=cookies,
                params=params
                )
            yield response
        except Exception as e:
            # logger.error(response)
            continue
    
def response_to_filtered_json(response):
    json_response = response.json()
    mailing_events = json_response['sendungen']['key_to_be_figured_out']
    return mailing_events

def mailing_events_to_df(mailing_events):
    normalized_mailing_events = pd.json_normalize(mailing_events)
    mail_ids_df = pd.concat(
                            [mail_ids_df,normalized_mailing_events],
                            ignore_index=True
                            )
    return mail_ids_df

def df_to_excel(df, excel_name):
    # mail_ids_df.to_excel('mail_ids_data.xlsx')
    df.to_excel(f'excel_name.xlsx')