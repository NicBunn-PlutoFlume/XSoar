
import pytest

import demistomock as demisto
from Tessian import (
    format_url,
    Client,
    get_events_command,
    release_from_quarantine_command,
    delete_from_quarantine_command,
    fetch_incidents,
)

#  region HELPERS


def create_mock_client():
    return Client(
        base_url='https://api.example.com',
        verify=False,
        headers={
            'Authentication': 'API-Token some_api_key'
        }
    )

#  endregion


def test_fetch_incidents(mocker):
    """
    Tests the fetch_incidents function.
    """
    client = create_mock_client()
    mocker.patch.object(
        client,
        'get_events',
        return_value={
            'checkpoint': "dummy_checkpoint",
            'additional_results': True,
            'results': [
                {
                    "id": "dummy_value",
                    "created_at": "dummy_value",
                },
            ],
        }
    )

    fetch_incidents(client, 100)

    assert demisto.setLastRun.call_args[0][0]['checkpoing'] == 'dummy_checkpoint'


def test_get_events_command(mocker):
    """
    Tests the get_events_command function.
    """

    #  Mock the client
    client = create_mock_client()
    mocker.patch.object(
        client,
        'get_events',
        return_value={
            'checkpoint': "dummy_checkpoint",
            'additional_results': True,
            'results': [
                {
                    "dummy_key": "dummy_value"
                },
            ],
        }
    )

    input = {
        "limit": 10,
        "after_checkpoint": None,
        "created_after": None,
    }

    response = get_events_command(client, input)

    assert response.outputs == {
        "checkpoint": "dummy_checkpoint",
        "additional_results": True,
        "results": {
            "dummy_key": "dummy_value",
        }
    }


def test_release_from_quarantine_comand(mocker):
    """
    Tests the release_from_quarantine_command function.
    """

    #  Mock the client
    client = create_mock_client()
    mocker.patch.object(
        client,
        'release_from_quarantine',
        return_value={
            "number_of_actions_attempted": 1,
            "number_of_actions_succeeded": 1,
            "results": [
                {
                    "user_address": "example@gmail.com",
                    "error": None,
                }
            ]
        }
    )

    input = {
        "event_id": "dummy_event_id",
    }

    response = release_from_quarantine_command(client, input)

    assert response.outputs == {
        "number_of_actions_attempted": 1,
        "number_of_actions_succeeded": 1,
        "results": [
            {
                "user_address": "example@gmail.com",
                "error": None,
            },
        ]
    }


def test_delete_from_quarantine_command(mocker):
    """
    Tests the delete_from_quarantine_command function.
    """

    #  Mock the client
    client = create_mock_client()
    mocker.patch.object(
        client,
        'delete_from_quarantine',
        return_value={
            "number_of_actions_attempted": 1,
            "number_of_actions_succeeded": 1,
            "results": [
                {
                    "user_address": "example@gmail.com",
                    "error": None,
                }
            ]
        }
    )

    input = {
        "event_id": "dummy_event_id",
    }

    response = delete_from_quarantine_command(client, input)

    assert response.outputs == {
        "number_of_actions_attempted": 1,
        "number_of_actions_succeeded": 1,
        "results": [
            {
                "user_address": "example@gmail.com",
                "error": None,
            },
        ]
    }


@pytest.mark.parametrize(
    """
    input_url, formatted_url
    """,
    [
        pytest.param(
            'https://test.com',
            'https://test.com',
            id='valid url given'
        ),
        pytest.param(
            'http://test.com',
            'https://test.com',
            id='http:// prefix given'
        ),
        pytest.param(
            'test.com',
            'https://test.com',
            id='no prefix given'
        ),
        pytest.param(
            'https://test.com/',
            'https://test.com',
            id='trailing slash given'
        ),
        pytest.param(
            'https://test.com/api/v1/test',
            'https://test.com',
            id='trailing url path given'
        ),
        pytest.param(
            'http://test.com/incorrect_api',
            'https://test.com',
            id='combination of incorrect prefix and suffix'
        ),
    ]
)
def test_format_url(input_url, formatted_url):
    assert formatted_url == format_url(input_url)
