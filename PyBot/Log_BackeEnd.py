import requests;
import json;
from requests.structures import CaseInsensitiveDict;
from dotenv import load_dotenv;
import os;
from requests.exceptions import ConnectionError;
from http.client import RemoteDisconnected;



class logging():

    
    def __init__(self):
        self.port = 8000;
        self.Token = {};
        print("Backend instance Created")

    def showToken(self):
        return self.Token;

    def getToken(self, userText, pswText):
        load_dotenv();
        baseUrl = os.getenv("Auth_URL"); ### PRODUCTIVO
        # baseUrl = f"http://localhost:{self.port}/"; ### -------- PRUEBAS --------------
        #proxies = {'https':'http://'+userText+':'+pswText+'@proxy-xm:8080'}
        endpoint = os.getenv("AUTH_ENDPOINT");
        url = baseUrl+endpoint;
        # print(f'url: {url}')

        headers = CaseInsensitiveDict();
        headers["accept"] = "*/*"
        headers["api-version"] = "1"
        headers["Authorization"] = "{validacion: 1,usuario: "+userText+",contrasena: "+pswText+"}"
        headers["Content-Type"] = "application/json"
        payload = '{"validacion":1,"usuario":"'+userText+'","contrasena":"'+pswText+'"}'

        try:
            #r = requests.post(urlA, headers=headers, data=payload, proxies=proxies)
            response = requests.post(url, headers=headers, data=payload); ### PRODUCTIVO
            # response = requests.get(url); ### -------- PRUEBAS --------------
            resp = response.json();
            # print(f"Response code: {r.status_code}");
            # print(f'Respuesta: {response}');
            if (response.status_code == 200):
                self.Token = json.loads(response.text);
                # print(f"Token: {self.Token['token']}");
            else:
                self.Token = {"error": resp};
                print(f"Se ha presentado error {response.status_code}: {resp}");
            return self.Token
        except(ConnectionError, RemoteDisconnected) as err:
            print("Se ha presentado Error: ", err);
            self.Token = {"error": err}
            return self.Token


    def getData(self, date):
        Token = self.Token;
        # print('Token usado: ', Token);
        load_dotenv();
        baseUrl = os.getenv("MANEUVER_URL"); ### PRODUCTIVO
        # baseUrl = f"http://localhost:{self.port}/"; ### -------- PRUEBAS --------------
        #proxies = {'https':'http://'+userText+':'+pswText+'@proxy-xm:8080'}
        endpoint = os.getenv("ACTIONS_ENDPOINT");
        actionsNumber = 100
        url = baseUrl+endpoint;
        # print(f'url: {url}')
        headers = CaseInsensitiveDict();
        headers["accept"] = "*/*"
        headers["Content-Type"] = "application/json"
        if('token' in Token.keys()):
            headers = {'Authorization': 'Bearer ' + Token['token']}
            baseUrl = os.getenv("MANEUVER_URL");
            endpoint = os.getenv("ACTION_ENDPOINT");
            #dFec = dt.datetime.strptime(self.ui.entFecha.text(), "%Y-%m-%d")
            #dCsl = dFec.strftime('%Y-%m-%d')
            JSONpayload = {
                "dateFrom": date + " 00:00",
                "dateTo": date + " 23:59:00",
                "statusIds": [],
                "systems": [],
                "elementIds": [],
                "elementCompanyNames": [],
                "elementTypeIds": [],
                "actionTypeIds": [],
                "originPanelIds": [],
                "sourceCND": "true",
                "sourceAgents": "true",
                "limitTo": actionsNumber,
                "showCneZniElementDetail":"true" 
            } 
            # payload = json.dumps(JSONpayload);
            response = requests.post(url, headers=headers, json=JSONpayload);  ### PRODUCTIVO #json para usar json, data para usar cadena de string.
            # response = requests.get(url); ### -------- PRUEBAS --------------
            resp = response.json();
            # print("Atributos: ", resp[0].keys());
            # Atributos disponibles: ['id', 'actionTypeId', 'actionType', 'flowId', 'flow', 'flowConsecutive', 'scheduledStartDate', 'elementId', 'elementTypeId', 'elementName', 'elementCompanyName', 'elementCompanyShortName', 'instructionTime', 'occurrenceTime', 'confirmationTime', 'causeStatusId', 'causeStatus', 'consignmentId', 'causeChangeAvailabilityId', 'causeChangeAvailability', 'newAvailability', 'elementCausingId', 'causeSuspendedExecutionId', 'causeSuspendedExecution', 'fileDocumentNumber', 'associatedActionId', 'causeOperationalId', 'causeOperational', 'controlVQId', 'controlVQ', 'teleprotectionId', 'teleprotection', 'finalElement', 'percentage', 'instructionTimeChecked', 'occurrenceTimeChecked', 'confirmationTimeChecked', 'order', 'parentTimeActionId', 'parentTypeTimeAssociatedId', 'parentTypeTimeAssociated', 'typeTimeAssociatedId', 'typeTimeAssociated', 'withPriorAuthorization', 'isVoltageControl', 'hidden', 'description', 'verificationNote', 'statusTypeId', 'statusType', 'locked', 'lockedByActionId', 'system', 'originPanelId', 'originPanel', 'causeOrigin', 'causeDetailCno', 'additionalFieldsValue', 'dashboardOrderingDate', 'espId', 'espName', 'espElementId', 'creationTime', 'filterActionOrderingDate', 'unavailableActionId', 'subSystemUnavailableAction', 'cneZone', 'fuel', 'fuelName', 'fuelCEN', 'plantCEN', 'qualityScheme', 'notification', 'reverseNotificationGenerated', 'source', 'disableAvailabilityField', 'dna', 'userValidator', 'configurationId', 'configurationDesc', 'thermalStateId', 'descriptionAdditional']
            # Atributos de interés: ['id', 'actionTypeId', 'actionType', 'flowId', 'flow', 'flowConsecutive', 'scheduledStartDate', 'elementId', 'elementName', 'elementCompanyShortName', 'instructionTime', 'occurrenceTime', 'confirmationTime', 'causeStatus', 'consignmentId', 'causeChangeAvailability', 'newAvailability', 'elementCausingId', 'causeOperational', 'percentage', 'order', 'withPriorAuthorization', 'isVoltageControl', 'description', 'verificationNote', 'statusType', 'system', 'originPanel', 'causeOrigin', 'causeDetailCno', 'additionalFieldsValue', 'espName', 'espElementId', 'creationTime', 'unavailableActionId', 'subSystemUnavailableAction', 'cneZone', 'fuel', 'fuelName', 'fuelCEN', 'plantCEN', 'qualityScheme', 'source','dna', 'userValidator', 'configurationDesc', 'thermalStateId', 'descriptionAdditional']
        else:
            # resp = json.dumps({"error": "Autenticación expirada. Vuelva a autenticarse."}, indent=4, sort_keys=True, ensure_ascii=False);
            resp = {"error": "Autenticación expirada. Vuelva a autenticarse."};
        # print(f'GetData response: {resp}');
        return resp;
        
    def logIn(self, userEntry, pswEntry):
        infoText ="";
        userText = userEntry.get();
        pswText = pswEntry.get();
        Token = self.getToken(userText, pswText);
        
        if("error" in Token.keys()):
            infoText = Token["error"]; 
        # self.getData(Token, date)
        #headers = {"Authorization": "Bearer MYREALLYLONGTOKENIGOT"}
        # text1.delete("1.0", END);
        # text1.insert(END, entryG);
        userEntry.set("");
        pswEntry.set("");
        return infoText;