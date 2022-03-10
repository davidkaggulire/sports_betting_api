# test.py

import pytest
import wsgi as app


headers = {'Content-Type': 'application/json', 'api-key': '1234'}
test_data = {
    "league": "Premier",
    "home_team": "Chelsea",
    "away_team": "Liverpool",
    "home_team_win_odds": 4.0,
    "away_team_win_odds": 5.0,
    "draw_odds": 4.0,
    "game_date": "2022-01-12"
}

missing_data = {
    "league": "Premier",
    "home_team": "",
    "away_team": "Liverpool",
    "home_team_win_odds": 4.0,
    "away_team_win_odds": 5.0,
    "draw_odds": 4.0,
    "game_date": "2022-01-12"
}


@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    client = app.app.test_client()
    yield client


def test_create_odds_while_not_authenitcated(client):
    response = client.post('/api/v1/odds', json=test_data)
    json_data = response.get_json()

    assert json_data['message'] == 'API key required'
    assert response.status_code == 403


def test_create_odds_with_correct_data_and_authenticated(client):
    response = client.post('/api/v1/odds', json=test_data, headers=headers)
    json_data = response.get_json()

    assert json_data['message'] == 'Odds created Successfully'
    assert response.status_code == 200


def test_create_odds_with_wrong_data(client):
    response = client.post('/api/v1/odds', json=missing_data, headers=headers)
    json_data = response.get_json()

    assert json_data['messages']['home_team'] == ['Shorter than minimum length 1.']
    assert response.status_code == 403


def test_read_odds_while_not_authenitcated(client):
    data = {
        "league": "Premier",
        "date_range": "2021-12-31 to 2022-02-15"
    }
    response = client.post('/api/v1/odds/read', json=data)
    json_data = response.get_json()

    assert json_data['message'] == 'API key required'
    assert response.status_code == 403


def test_read_odds_while_authenitcated(client):
    data = {
        "league": "Premier",
        "date_range": "2021-12-31 to 2022-02-15"
    }
    client.post('/api/v1/odds', json=test_data, headers=headers)
    response = client.post('/api/v1/odds/read', json=data, headers=headers)
    json_data = response.get_json()

    assert json_data['message'] == 'Odds read successfully'
    assert response.status_code == 200


def test_read_odds_that_dont_exist(client):
    data = {
        "league": "Premier",
        "date_range": "2023-12-31 to 2024-02-15"
    }
    response = client.post('/api/v1/odds/read', json=data, headers=headers)
    json_data = response.get_json()

    assert json_data['error'] == 'Odds Not found'
    assert response.status_code == 404


def test_read_odds_with_invalid_input_date_range(client):
    data = {
        "league": "Premier",
        "date_range": "12-12-2021 to 15-02-2022"
    }
    response = client.post('/api/v1/odds/read', json=data, headers=headers)
    json_data = response.get_json()

    assert json_data['message'] == 'Failed to read odds'
    assert response.status_code == 500


def test_update_odds_while_not_authenitcated(client):
    response = client.put('/api/v1/odds/1', json=test_data)
    json_data = response.get_json()

    assert json_data['message'] == 'API key required'
    assert response.status_code == 403


def test_update_odds_while_authenitcated(client):
    new_data = {
        "league": "Spanish",
        "home_team": "Celtic",
        "away_team": "Barcelona",
        "home_team_win_odds": 4.0,
        "away_team_win_odds": 5.0,
        "draw_odds": 4.0,
        "game_date": "2010-01-12"
    }
    response = client.post('/api/v1/odds', json=new_data, headers=headers)
    data = response.get_json()
    odds = data['odds']
    print(f"{odds} is the odds")
    odd_id = odds['id']

    update_data = {
        "league": "Spanish",
        "home_team": "Celtic",
        "away_team": "Atletico",
        "home_team_win_odds": 4.0,
        "away_team_win_odds": 5.0,
        "draw_odds": 4.0,
        "game_date": "2022-01-12"
    }

    response2 = client.put(f'/api/v1/odds/{odd_id}', json=update_data, headers=headers)
    json_data = response2.get_json()
    print(json_data)

    assert json_data['message'] == 'Odds updated successfully'
    assert response2.status_code == 200


def test_delete_odds_while_not_authenitcated(client):
    data = {
        "league": "Premier",
        "home_team": "Chelsea",
        "away_team": "Liverpool",
        "game_date": "2022-01-12"
    }
    response = client.delete('/api/v1/odds', json=data)
    json_data = response.get_json()

    assert json_data['message'] == 'API key required'
    assert response.status_code == 403


def test_delete_odds_while_authenitcated(client):
    data = {
        "league": "Spanish La Liga",
        "home_team": "Madrid",
        "away_team": "Atletico",
        "game_date": "2022-01-12"
    }

    post_data = {
        "league": "Spanish La Liga",
        "home_team": "Madrid",
        "away_team": "Atletico",
        "home_team_win_odds": 4.0,
        "away_team_win_odds": 5.0,
        "draw_odds": 4.0,
        "game_date": "2022-01-12"
    }
    client.post('/api/v1/odds', json=post_data, headers=headers)
    response = client.delete('/api/v1/odds', json=data, headers=headers)
    json_data = response.get_json()

    assert json_data['message'] == 'Odds deleted successfully'
    assert response.status_code == 200


def test_delete_odds_not_found(client):
    data = {
        "league": "Spanish La Liga",
        "home_team": "Madrid",
        "away_team": "Atletico",
        "game_date": "2023-01-12"
    }

    client.post('/api/v1/odds', json=test_data, headers=headers)
    response = client.delete('/api/v1/odds', json=data, headers=headers)
    json_data = response.get_json()

    assert json_data['message'] == 'odds not found'
    assert response.status_code == 404


def test_delete_invalid_input(client):
    data = {
        "league": "Spanish La Liga",
        "home_team": "Madrid",
        "away_team": "Atletico",
        "game_date": "12-01-2022"
    }

    post_data = {
        "league": "Spanish La Liga",
        "home_team": "Madrid",
        "away_team": "Atletico",
        "home_team_win_odds": 4.0,
        "away_team_win_odds": 5.0,
        "draw_odds": 4.0,
        "game_date": "2022-01-12"
    }

    client.post('/api/v1/odds', json=post_data, headers=headers)
    response = client.delete('/api/v1/odds', json=data, headers=headers)
    json_data = response.get_json()
    print(json_data)

    assert json_data['messages']['game_date'] == ["Not a valid date."]
    assert response.status_code == 403
