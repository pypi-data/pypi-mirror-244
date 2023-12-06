import requests

def generate_key(params, debug):
    url = 'https://pandadevelopment.net/serviceapi/generate-key/'
    response = requests.post(url, params=params)
    if debug:
      print(f"[Debug] Response : {response} , StatusCode : {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        if debug:
          print(f"[Debug] Data : {data}")
        if (
            data.get('message') == 'Keys generated successfully ✅' and
            isinstance(data.get('generatedKeys'), list) and
            len(data.get('generatedKeys')) > 0 and
            data.get('generatedKeys')[0].get('value')
        ):
            generated_key = data.get('generatedKeys')[0].get('value')
            print(f"[Debug] Generated key : {generated_key}")
            return generated_key
        else:
            return 'Unexpected response format: {}'.format(data)
    else:
        return 'Request failed with status code: {}'.format(response.status_code)