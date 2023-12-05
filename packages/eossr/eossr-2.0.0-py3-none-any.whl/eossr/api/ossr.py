#!/usr/bin/env python

import requests

from .zenodo import ZenodoAPI, query_records, search_records

__all__ = [
    'search_ossr_records',
    'get_ossr_records',
    'get_ossr_pending_requests',
]

escape_community = 'escape2020'
sandbox_escape_community = 'escape2020'


def search_ossr_records(search='', sandbox=False, **kwargs):
    """
    Search the OSSR for records whose names or descriptions include the provided string `search`.
    The default record type is 'software' or 'record'.

    :param search: string
        A string to refine the search in the OSSR. The default will search for all records in the OSSR.
    :param sandbox: bool
        Indicates the use of sandbox zenodo or not.
    :param kwargs: Zenodo query arguments.
        For an exhaustive list, see the query arguments at https://developers.zenodo.org/#list36
        Common arguments are:
        - size: int
        Number of results to return. Default = 100
        - all_versions: int
        Show (1) or hide (0) all versions of records
        - type: string or list[string]
        Default: ['software', 'dataset']
        Records of the specified type (Publication, Poster, Presentation, Software, ...).
        A logical OR is applied in case of a list
        - subject: string or list[string]
        Records with the specified keywords. A logical OR is applied in case of a list
        - file_type: string or list[string]
        Records from the specified file_type. A logical OR is applied in case of a list

    :return: [Record]
    """

    # make sure we find all OSSR records without limit on the number
    params = kwargs
    params['communities'] = escape_community
    response = query_records(search, sandbox=sandbox, **params)
    number_of_ossr_entries = response.json(
    )['aggregations']['access_status']['buckets'][0]['doc_count']
    kwargs['size'] = number_of_ossr_entries

    # if another community is specified, a logical OR is applied by zenodo API,
    # thus potentially finding entries that are not part of escape2020
    # ruling out that possibility at the moment
    if 'communities' in kwargs and kwargs['communities'] != escape_community:
        raise NotImplementedError(
            "Searching in another community will search outside of the OSSR"
            "Use `eossr.api.zenodo.search_records` to do so"
        )
    kwargs['communities'] = escape_community

    # OSSR is limited to software and datasets
    kwargs.setdefault('type', ['software', 'dataset'])

    return search_records(search, sandbox=sandbox, **kwargs)


def get_ossr_pending_requests(**params):
    """
    Get a list of records that have been requested to be added to the OSSR.

    :param params: dict
        Parameters for the request. Override the class parameters.
    :return:
    """
    zen = ZenodoAPI()
    return zen.get_community_pending_requests(escape_community, **params)


def get_ossr_records(sandbox=False, **kwargs):
    """
    Get a list of records that have been added to the OSSR.

    :return:
    """
    return search_ossr_records('', sandbox=sandbox, **kwargs)
