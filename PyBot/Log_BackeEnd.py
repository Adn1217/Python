import requests;
import json;
from requests.structures import CaseInsensitiveDict;
from dotenv import load_dotenv;
import os;



class logging():
    Token = None;

    def __init__(self):
        print("Instance Created")

    def getToken(self, userText, pswText):
        load_dotenv();
        baseUrl = os.getenv("Auth_URL");
        #proxies = {'https':'http://'+userText+':'+pswText+'@proxy-xm:8080'}
        endpoint = os.getenv("AUTH_ENDPOINT");
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
        print(f"R: {r.status_code}");
        # print(f'Respuesta: {response}');
        if (r.status_code == 200):
            Token = json.loads(r.text);
            print(f"Token: {Token['token']}");
        else:
            Token = {"error": response};
            print(f"Se ha presentado error {r.status_code}: {response}");
        return Token

    def getData(self, Token, date):
        load_dotenv();
        #baseUrl = os.getenv("MANEUVER_URL");
        port = 8000;
        baseUrl = f"http://localhost:{port}/";
        #proxies = {'https':'http://'+userText+':'+pswText+'@proxy-xm:8080'}
        endpoint = os.getenv("ACTIONS_ENDPOINT");
        url = baseUrl+endpoint;
        print(f'url: {url}')
        headers = CaseInsensitiveDict();
        headers["accept"] = "text/plain"
        headers = {'Authorization': 'Bearer ' + Token['token']}
        headers["Content-Type"] = "application/json"
        baseUrl = os.getenv("MANEUVER_URL");
        endpoint = os.getenv("ACTION_ENDPOINT");
        #dFec = dt.datetime.strptime(self.ui.entFecha.text(), "%Y-%m-%d")
        #dCsl = dFec.strftime('%Y-%m-%d')
        JSONpayload = {
            "dateFrom": "2025-05-23T00:00:00.000Z",
            "dateTo": "2025-05-23T00:00:00.000Z",
            "statusIds": [],
            "systems": [],
            "elementIds": [],
            "elementCompanyNames": [],
            "elementTypeIds": [],
            "actionTypeIds": [],
            "originPanelIds": [],
            "sourceCND": "true",
            "sourceAgents": "true",
            "limitTo": 10,
            "showCneZniElementDetail":"true" 
        } 
        payload = json.dumps(JSONpayload);
        # r = requests.post(url, headers=headers, data=payload);
        r = requests.get(url);
        print(f'GetData response: {r.json()}');
        
    def logIn(self, userEntry, pswEntry):
        infoText ="";
        userText = userEntry.get();
        pswText = pswEntry.get();
        Token = self.getToken(userText, pswText);
        # Token = {
        #     "token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjUwNDEyIiwiSWRVc3VhcmlvIjoiMTYzIiwiUm9sZXMiOiJYTV9HX0NlbnRyb0NvbnRyb2xDTkQsWE0tRy1JU0UtVXN1YXJpb3MsWE1fR19EQ08sU0lPX0FnZW50ZV9Db25zdWx0YSxTSU9fQ29uc3VsdGFfWE0sU0lPX0FnZW50ZV9UcmFuc3BvcnRhZG9yX0dlbmVyYWRvcixTSU9fQW5hbGlzdGFfWE0sU0lPX0FkbWluaXN0cmFkb3JfWE0sWE1fR19DZW50cm9Db250cm9sX0luZm9IZXJvcGUsU0lPX09QX0NvbnN1bHRhX1hNLFNJT19PUF9BbmFsaXN0YV9YTSxTSU9fT1BfQWdlbnRlX1RyYW5zcG9ydGFkb3JfR2VuZXJhZG9yLFNJT19PUF9BZ2VudGVfQ29uc3VsdGEsU0lPX09QX0FkbWluaXN0cmFkb3JfWE0sWE1QSV9MZWN0dXJhLFBhY3RvIENvbGVjdGl2byBYTSxBbnRpZ2VuYV9YTSxNREMtQ09OU1VMVEEsTURDLUFETUlOLVBBUkFNRVRST1MsTURDLUlOVEVHUkFDSU9ORVMsUkFTLUVNUExFQURPUyxHUlBfREVPVFIsUlBBR0VDX0hFUk9QRSxhZG1pbmlzdHJhZG9yUmVkZXNwYWNobyxIZXJvcGVPcGVyYWRvckNORCxDT05TSVRWVyxDT05TSVRBRE1JTixMZWN0dXJhX1B1YmxpY29LLEFjY2Vzb0NvbW1hbmRQcm9tcHQsQW5hbGlzdGFyZWRlc3BhY2hvLFNQRU1fQURNSU4sU1BFTV9DT05TVSxPcGVyYWRvciBDTkQsUEVSU09OQUwgR0VSRU5DSUEgQ05ELElETyxQQVJBVEVDLENlbnRyb2RlY29udHJvbCxDZW50cm8gZGUgQ29udHJvbCBDTkQsQ2xpZW50ZXMgSW50ZXJub3MgQkksVXN1YXJpb3NEUlAsVXN1YXJpb3NYTSxQZXJzb25hbCBYTSIsIk5vbWJyZUNvbXBsZXRvIjoiQURSScOBTiBBTEJFUlRPIEZFUk7DgU5ERVogQ0FCUkVSQSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6WyJYTV9HX0NlbnRyb0NvbnRyb2xDTkQiLCJYTS1HLUlTRS1Vc3VhcmlvcyIsIlhNX0dfRENPIiwiU0lPX0FnZW50ZV9Db25zdWx0YSIsIlNJT19Db25zdWx0YV9YTSIsIlNJT19BZ2VudGVfVHJhbnNwb3J0YWRvcl9HZW5lcmFkb3IiLCJTSU9fQW5hbGlzdGFfWE0iLCJTSU9fQWRtaW5pc3RyYWRvcl9YTSIsIlhNX0dfQ2VudHJvQ29udHJvbF9JbmZvSGVyb3BlIiwiU0lPX09QX0NvbnN1bHRhX1hNIiwiU0lPX09QX0FuYWxpc3RhX1hNIiwiU0lPX09QX0FnZW50ZV9UcmFuc3BvcnRhZG9yX0dlbmVyYWRvciIsIlNJT19PUF9BZ2VudGVfQ29uc3VsdGEiLCJTSU9fT1BfQWRtaW5pc3RyYWRvcl9YTSIsIlhNUElfTGVjdHVyYSIsIlBhY3RvIENvbGVjdGl2byBYTSIsIkFudGlnZW5hX1hNIiwiTURDLUNPTlNVTFRBIiwiTURDLUFETUlOLVBBUkFNRVRST1MiLCJNREMtSU5URUdSQUNJT05FUyIsIlJBUy1FTVBMRUFET1MiLCJHUlBfREVPVFIiLCJSUEFHRUNfSEVST1BFIiwiYWRtaW5pc3RyYWRvclJlZGVzcGFjaG8iLCJIZXJvcGVPcGVyYWRvckNORCIsIkNPTlNJVFZXIiwiQ09OU0lUQURNSU4iLCJMZWN0dXJhX1B1YmxpY29LIiwiQWNjZXNvQ29tbWFuZFByb21wdCIsIkFuYWxpc3RhcmVkZXNwYWNobyIsIlNQRU1fQURNSU4iLCJTUEVNX0NPTlNVIiwiT3BlcmFkb3IgQ05EIiwiUEVSU09OQUwgR0VSRU5DSUEgQ05EIiwiSURPIiwiUEFSQVRFQyIsIkNlbnRyb2RlY29udHJvbCIsIkNlbnRybyBkZSBDb250cm9sIENORCIsIkNsaWVudGVzIEludGVybm9zIEJJIiwiVXN1YXJpb3NEUlAiLCJVc3Vhcmlvc1hNIiwiUGVyc29uYWwgWE0iXSwibmJmIjoxNzQ4MTM1NDgzLCJleHAiOjE3NDgxMzY2ODMsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6NjE4MDYvIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo2MTgwNi8ifQ.aQQaQdfFnGx3wBmhYsiPT0klg72AjhwQAd-uHWgFe4Y"
        # }
        
        if("error" in Token.keys()):
            infoText = Token["error"]; 
        date ="05/19/2025 00:00"
        # self.getData(Token, date)
        #headers = {"Authorization": "Bearer MYREALLYLONGTOKENIGOT"}
        # text1.delete("1.0", END);
        # text1.insert(END, entryG);
        userEntry.set("");
        pswEntry.set("");
        return infoText;