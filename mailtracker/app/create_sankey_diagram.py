import pandas as pd

def gen_sankey(df, selected_columns=None, filter=None,
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