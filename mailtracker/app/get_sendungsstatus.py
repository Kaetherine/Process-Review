#%%
import requests
import pandas as pd

def get_sendungsstatus():
    #%%
    # request url
    url = "https://www.deutschepost.de/int-verfolgen/data/search"

    #%%
    # header and cookie settings
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "referer": "https://www.deutschepost.de/de/s/sendungsverfolgung.html",
    }

    #%%
    cookies = {
        "verfolgenSL": "eyJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiZGlyIn0..-R6mTuXgyZcvLd4X32eEMw...",
        "_abck": "6280D482FE82DB5DE5656B88A63F313D~0~YAAQlKAkFwlgx9WSAQAAaGHW4QwxrrC...",
        "bm_sv": "8C9E8E77137677EB5555599BA65BC2A6~YAAQlKAkFztpx9WSAQAAVJ/W4RmDX45e...",
    }

    #%%
    sendungsnummern = [

        'A005BCE237000000003E',
        'A005BCE2370000000047',

        ]

    #%%
    sendungsnummern_data_df = pd.DataFrame()

    # %%
    for sendungsnummer in sendungsnummern:
        params = {
            'piececode': sendungsnummer,
            'inputSearch': 'true',
            'language': 'de'
        }
        #get-request
        response = requests.get(
            url,
            headers=headers,
            cookies=cookies,
            params=params
            )

        if response.status_code == 200:
            response_data = response.json()
            response_data_sendungen = response_data['sendungen']
            normalized = pd.json_normalize(response_data_sendungen)
            sendungsnummern_data_df = pd.concat([
                sendungsnummern_data_df, normalized],
                ignore_index=True)
        else:
            print(f"Error: {response.status_code}, Message: {response.text}")

    #%%
    sendungsnummern_data_df.to_excel('sendungsnummern_data.xlsx')

#%%