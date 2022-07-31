import requests
import json

def token_generate():
    print("Hello!!!!")
    client_id = '013c09ebef829ae93ee3'
    client_secret = '3f7011b36e9eeb25c8c3fe9be2bcac20'

        # initiate the request to get the token 
    r = requests.post("https://api.artsy.net/api/tokens/xapp_token",
        data={
            "client_id": client_id,
            "client_secret": client_secret
        })

        # parse the server response 
    j = json.loads(r.text)

        # extract the token 
    token = j["token"]
    print("token that I jusst fetched: ", token)

    return token

def get_code():
    res = requests.get('https://www.deviantart.com/oauth2/authorize?response_type=code&client_id=17521&redirect_uri=http://127.0.0.1:5000/login/google/Home1&scope=basic&state=mysessionid').json()
    # print(json.loads(res.text))
    print("we got the code!!")
    