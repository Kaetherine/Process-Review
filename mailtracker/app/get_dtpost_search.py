import requests
import pandas as pd


# mail_ids = [
#         'A005BCE237000000003E',
#         'A005BCE2370000000047',
#         ]

def get_sendungsstatus(mail_ids):
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
            # logger.info(response)
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

# mail_ids_df.to_excel('mail_ids_data.xlsx')