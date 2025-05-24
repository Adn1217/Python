import requests;
import json;
from requests.structures import CaseInsensitiveDict;
from dotenv import load_dotenv;
import os;



class logging():

    def __init__(self):
        print("Instance Created")

    def getToken(self, userText, pswText):
        load_dotenv();
        baseUrl = os.getenv("Auth_URL");
        #proxies = {'https':'http://'+userText+':'+pswText+'@proxy-xm:8080'}
        print(f'AutBaseurl: {baseUrl}')
        endpoint = os.getenv("AUTH_ENDPOINT");
        print(f'AutEndpoint: {endpoint}')
        url = baseUrl+endpoint;
        print(f'url: {url}')

        headers = CaseInsensitiveDict();
        headers["accept"] = "*/*"
        headers["api-version"] = "1"
        headers["Authorization"] = "{validacion: 1,usuario: "+userText+",contrasena: "+pswText+"}"
        headers["Content-Type"] = "application/json"
        payload = '{"validacion":1,"usuario":"'+userText+'","contrasena":"'+pswText+'"}'

        
        #r = requests.post(urlA, headers=headers, data=payload, proxies=proxies)
        r = requests.post(url, headers=headers, data=payload);
        response = r.json();

        Token = json.loads(r.text);
        print(f"Token: {Token['token']}");
        return Token

    def getData(self, Token, date):
        headers = CaseInsensitiveDict();
        headers["accept"] = "text/plain"
        headers = {'Authorization': 'Bearer ' + Token['token']}
        headers["Content-Type"] = "application/json"
        baseUrl = os.getenv("MANEUVER_URL");
        endpoint = os.getenv("ACTION_ENDPOINT");
        url = baseUrl+endpoint;
        #dFec = dt.datetime.strptime(self.ui.entFecha.text(), "%Y-%m-%d")
        #dCsl = dFec.strftime('%Y-%m-%d')
        payload = {
            }
        r = requests.post(url, headers=headers, json=payload);
        
    def logIn(self, userEntry, pswEntry):
        userText = userEntry.get();
        pswText = pswEntry.get();
        Token = self.getToken(userText, pswText);
        date ="05/19/2025 00:00"
        #self.getData(Token, date)
        #headers = {"Authorization": "Bearer MYREALLYLONGTOKENIGOT"}
        print("Usuario: ", userText);
        print("Contraseña: ", pswText);
        # text1.delete("1.0", END);
        # text1.insert(END, entryG);
        # text2.delete("1.0", END);
        # text2.insert(END, entryP);
        # text3.delete("1.0", END);
        # text3.insert(END, entryO);
        userEntry.set("");
        pswEntry.set("");