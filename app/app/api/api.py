# coding=utf-8
from flask import request
from datetime import datetime
import json
from .utils import get_point
from ..main import app
from ..core.database import get_postal_code_id_from_db, get_turnover_by_month_gender_from_db, get_postal_code_from_db, \
    get_map_from_db, get_total_turnover_from_db, get_turnover_by_age_gender_from_db


@app.route('/v0/turnover/by-month-gender', methods=['GET'])
def get_turnover_by_month_gender():
    """
    Serves Turnover by date and gender at the point x.y.
    :url_params: point (lat float,long float)
    :url_example: v0/turnover/by-age-gender?point=40.4,-3.7
    :returns
    """
    # TODO: Add date range filters

    # get the point
    try:
        lat, lon = get_point(request)
    except Exception as e:
        return {'status': 'error', 'message': 'Not a valid point. ' + str(e)}

    # Get postal code id
    postal_code_id = get_postal_code_id_from_db(lat, lon)
    # Get tht postal code
    postal_code = get_postal_code_from_db(postal_code_id)
    # Get the data
    results = get_turnover_by_month_gender_from_db(postal_code_id)

    if len(results) == 0:
        return {'status': 'error', 'message': 'No data could be retrieved'}

    data = {'F': [], 'M': []}
    for result in results:
        data[result[1]].append([datetime.strptime(result[0], '%Y-%m-%d').timestamp(), result[2]])
    return {'label': 'Turnover by Month and Gender', 'ZIPCODE': postal_code,
            'currency': u"€", 'status': 'ok',
            'series': [{'data': data['F'], 'name': 'Female', 'tooltip':{'valuesSuffix': ' €'}},
                       {'data': data['M'], 'name': 'Male', 'tooltip':{'valuesSuffix': ' €'}}]}


@app.route('/v0/turnover/by-age-gender', methods=['GET'])
def get_turnover_by_age_gender():
    # get the point
    try:
        lat, lon = get_point(request)
    except Exception as e:
        return {'status': 'error', 'message': 'Not a valid point. ' + str(e)}

    # Get postal code id
    postal_code_id = get_postal_code_id_from_db(lat, lon)
    # Get tht postal code
    postal_code = get_postal_code_from_db(postal_code_id)
    # Get the data
    results = get_turnover_by_age_gender_from_db(postal_code_id)

    if len(results) == 0:
        return {'status': 'error', 'message': 'No data could be retrieved'}
    data = {'F': [], 'M': []}
    for result in results:
        data[result[1]].append([result[0], result[2]])
    return {'label': 'Turnover by Age and Gender', 'ZIPCODE': postal_code,
            'currency': u"€", 'status': 'ok',
            'series': [{'data': data['F'], 'name': 'Female', 'tooltip': {'valuesSuffix': ' €'}},
                       {'data': data['M'], 'name': 'Male', 'tooltip': {'valuesSuffix': ' €'}}]
            }


@app.route('/v0/turnover/total', methods=['GET'])
def get_total_turnover():
    # get the point
    try:
        lat, lon = get_point(request)
    except Exception as e:
        return {'status': 'error', 'message': 'Not a valid point. ' + str(e)}

    # Get postal code id
    postal_code_id = get_postal_code_id_from_db(lat, lon)
    # Get tht postal code
    postal_code = get_postal_code_from_db(postal_code_id)
    # Get the data
    results = get_total_turnover_from_db(postal_code_id)

    if results is None:
        return {'status': 'error', 'message': 'No data could be retrieved'}

    return {'label': 'Total Turnover', 'ZIPCODE': postal_code,
            'currency': u"€", 'status': 'ok', 'turnover': results}


@app.route('/v0/map/turnover/com_madrid.geo.json', methods=['GET'])
def get_map_com_madrid():
    """
    Serves the geometries for the Comunidad de Madrid with turnover info.
    """
    cmmap = [{'type': 'Feature', 'geometry': json.loads(feature[1]),
              'properties': {'zip_code': feature[0], 'turnover': feature[2]}}
             for feature in get_map_from_db('28%')]

    return {'type': 'FeatureCollection', 'features': cmmap}
