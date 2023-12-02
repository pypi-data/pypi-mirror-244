import requests


def fetch_response(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            json_data = response.json()
            return json_data
        else:
            return f"Error: Unable to retrieve data. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
