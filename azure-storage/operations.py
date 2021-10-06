""" Copyright start
  Copyright (C) 2008 - 2021 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

from requests import request, exceptions as req_exceptions
from .microsoft_api_auth import *

logger = get_logger('azure-storage')

storage_api_endpoint = 'https://management.azure.com'


def api_request(method, endpoint, connector_info, config, params=None, data=None, headers={}):
    try:
        ms = MicrosoftAuth(config)
        token = ms.validate_token(config, connector_info)
        headers['Authorization'] = token
        headers['Content-Type'] = 'application/json'
        logger.debug("Endpoint: {0}".format(endpoint))
        try:
            response = request(method, endpoint, headers=headers, params=params, json=data, verify=ms.verify_ssl)
            logger.debug("Response Status Code: {0}".format(response.status_code))
            logger.debug("Response: {0}".format(response.text))
            logger.debug("API Header: {0}".format(response.headers))
            if response.status_code in [200, 201, 204]:
                if response.text != "":
                    return response.json()
                else:
                    return True
            else:
                if response.text != "":
                    err_resp = response.json()
                    failure_msg = err_resp['error']['message']
                    error_msg = 'Response [{0}:{1} Details: {2}]'.format(response.status_code, response.reason,
                                                                         failure_msg if failure_msg else '')
                else:
                    error_msg = 'Response [{0}:{1}]'.format(response.status_code, response.reason)
                logger.error(error_msg)
                raise ConnectorError(error_msg)
        except req_exceptions.SSLError:
            logger.error('An SSL error occurred')
            raise ConnectorError('An SSL error occurred')
        except req_exceptions.ConnectionError:
            logger.error('A connection error occurred')
            raise ConnectorError('A connection error occurred')
        except req_exceptions.Timeout:
            logger.error('The request timed out')
            raise ConnectorError('The request timed out')
        except req_exceptions.RequestException:
            logger.error('There was an error while handling the request')
            raise ConnectorError('There was an error while handling the request')
        except Exception as err:
            raise ConnectorError(str(err))
    except Exception as err:
        raise ConnectorError(str(err))


def check_payload(payload):
    final_payload = {}
    for key, value in payload.items():
        if isinstance(value, dict):
            nested = check_payload(value)
            if len(nested.keys()) > 0:
                final_payload[key] = nested
        elif value:
            final_payload[key] = value
    return final_payload


def build_payload(payload):
    payload = {k: v for k, v in payload.items() if v is not None and v != ''}
    return payload


def list_storage_accounts(config, params, connector_info):
    try:
        endpoint = storage_api_endpoint + '/subscriptions/{0}/providers/Microsoft.Storage/storageAccounts?api-version=2021-04-01'.format(
            params.get('subscriptionId'))
        response = api_request("GET", endpoint, connector_info, config)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def get_storage_account(config, params, connector_info):
    try:
        endpoint = storage_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Storage/storageAccounts/{2}?api-version=2021-04-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('accountName'))
        response = api_request("GET", endpoint, connector_info, config)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def update_storage_account(config, params, connector_info):
    try:
        endpoint = storage_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Storage/storageAccounts/{2}?api-version=2021-04-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('accountName'))
        additional_fields = params.get('additional_fields')
        payload = {}
        if additional_fields:
            payload.update(additional_fields)
        payload = check_payload(payload)
        logger.debug("Payload: {0}".format(payload))
        response = api_request("PATCH", endpoint, connector_info, config, data=payload)
        if response:
            return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def delete_storage_account(config, params, connector_info):
    try:
        endpoint = storage_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Storage/storageAccounts/{2}?api-version=2021-04-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('accountName'))
        response = api_request("DELETE", endpoint, connector_info, config)
        return {'result': 'Storage Account {0} successfully Deleted'.format(params.get('accountName'))}
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def list_blob_services(config, params, connector_info):
    try:
        endpoint = storage_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Storage/storageAccounts/{2}/blobServices?api-version=2021-04-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('accountName'))
        response = api_request("GET", endpoint, connector_info, config)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def get_blob_service_properties(config, params, connector_info):
    try:
        endpoint = storage_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Storage/storageAccounts/{2}/blobServices/default?api-version=2021-04-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('accountName'))
        response = api_request("GET", endpoint, connector_info, config)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def set_blob_service_properties(config, params, connector_info):
    try:
        endpoint = storage_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Storage/storageAccounts/{2}/blobServices/default?api-version=2021-04-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('accountName'))
        additional_fields = params.get('additional_fields')
        payload = {}
        if additional_fields:
            payload.update(additional_fields)
        payload = check_payload(payload)
        logger.debug("Payload: {0}".format(payload))
        response = api_request("PUT", endpoint, connector_info, config, data=payload)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def create_blob_container(config, params, connector_info):
    try:
        endpoint = storage_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Storage/storageAccounts/{2}/blobServices/default/containers/{3}?api-version=2021-04-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('accountName'), params.get('containerName'))
        additional_fields = params.get('additional_fields')
        payload = {}
        if additional_fields:
            payload.update(additional_fields)
        payload = check_payload(payload)
        logger.debug("Payload: {0}".format(payload))
        response = api_request("PUT", endpoint, connector_info, config, data=payload)
        if response:
            return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def update_blob_container(config, params, connector_info):
    try:
        endpoint = storage_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Storage/storageAccounts/{2}/blobServices/default/containers/{3}?api-version=2021-04-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('accountName'), params.get('containerName'))
        additional_fields = params.get('additional_fields')
        payload = {}
        if additional_fields:
            payload.update(additional_fields)
        payload = check_payload(payload)
        logger.debug("Payload: {0}".format(payload))
        response = api_request("PATCH", endpoint, connector_info, config, data=payload)
        if response:
            return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def list_blob_containers(config, params, connector_info):
    try:
        endpoint = storage_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Storage/storageAccounts/{2}/blobServices/default/containers?api-version=2021-04-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('accountName'))
        payload = {
            "$filter": params.get('$filter'),
            "$include": params.get('$include'),
            "$maxpagesize": params.get('$maxpagesize')
        }
        payload = build_payload(payload)
        logger.debug("Payload: {0}".format(payload))
        response = api_request("GET", endpoint, connector_info, config, params=payload)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def get_blob_container(config, params, connector_info):
    try:
        endpoint = storage_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Storage/storageAccounts/{2}/blobServices/default/containers/{3}?api-version=2021-04-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('accountName'), params.get('containerName'))
        response = api_request("GET", endpoint, connector_info, config)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def delete_blob_container(config, params, connector_info):
    try:
        endpoint = storage_api_endpoint + '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.Storage/storageAccounts/{2}/blobServices/default/containers/{3}?api-version=2021-04-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('accountName'), params.get('containerName'))
        response = api_request("DELETE", endpoint, connector_info, config)
        return {'result': 'Blob Container {0} successfully Deleted'.format(params.get('containerName'))}
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def _check_health(config, connector_info):
    try:
        return check(config, connector_info)
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


operations = {
    'list_storage_accounts': list_storage_accounts,
    'get_storage_account': get_storage_account,
    'update_storage_account': update_storage_account,
    'delete_storage_account': delete_storage_account,
    'list_blob_services': list_blob_services,
    'get_blob_service_properties': get_blob_service_properties,
    'set_blob_service_properties': set_blob_service_properties,
    'create_blob_container': create_blob_container,
    'update_blob_container': update_blob_container,
    'list_blob_containers': list_blob_containers,
    'get_blob_container': get_blob_container,
    'delete_blob_container': delete_blob_container
}
