import requests
import json
import math

def api_auth(auth_credentials):
    session_api = requests.Session()
    session_api.auth=(auth_credentials['username'], \
        auth_credentials['password'])
    return session_api

def api_query(session, endpoint, api_url='https://mois.metrosert.ee/api/v1',
        filter=None, method='GET'):
    if method in 'GET':
        return session.get(api_url + endpoint)
    else:
        return None

def api_get_instruments(session_api=None, company_id=64,
        auth_credentials=None, filter=None):
    result = {'data':None}
    if not session_api:
        if auth_credentials:
            session_api = api_auth(auth_credentials)
        else:
            return result
    response = api_query(session_api,
        '/customer/{}/instruments'.format(company_id))
    if response:
        dict_a = []
        instruments=response.json()
        for instrument in instruments['data']:
            dict_a.append(instrument)
        pages = instruments['paginator']['total_pages']
        if pages <= 1:
            return dict_a
        else:
            for i in range(2, pages):
                if filter:
                    resp_next = api_query(session_api,
                        '/customer/{}/instruments?{}&page={}' \
                            .format(company_id, filter, i))
                else:
                    resp_next = api_query(session_api,
                        '/customer/{}/instruments?page={}' \
                            .format(company_id, i))
                instruments=resp_next.json()
                for instrument in instruments['data']:
                    dict_a.append(instrument)
        result = {'data':dict_a}
    session_api = None
    return result
