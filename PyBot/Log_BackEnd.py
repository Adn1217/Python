"""This module handles backend operations for authentication and data retrieval."""  # pylint: disable=invalid-name

import json
import os
from http.client import RemoteDisconnected

import requests
from dotenv import load_dotenv
# from requests.exceptions import ConnectionError
from requests.structures import CaseInsensitiveDict


class BackEnd:
    """Class to handle backend operations for authentication and data retrieval."""

    def __init__(self, env, port):
        load_dotenv()
        self.env = env
        self.port = port
        self._token = {}

        if self.env == "prod":
            self.base_auth_url = os.getenv("AUTH_URL")
            self.base_actions_url = os.getenv("MANEUVER_URL")
        else:
            self.dev_base_url = str(os.getenv("URL_LOCAL")) + str(self.port) + "/"
            self.base_auth_url = self.dev_base_url
            self.base_actions_url = self.dev_base_url

        print(f"Backend instance Created in '{self.env}'.")

    def show_token(self):
        """Return the current authentication token."""
        return self._token

    def get_token(
        self, userText, pswText
    ) -> dict | ConnectionError | RemoteDisconnected:
        """Get the authentication token from the backend."""
        # baseUrl = os.getenv("Auth_URL"); ### PRODUCTIVO
        # baseUrl = f"http://localhost:{self.port}/"; ### -------- PRUEBAS --------------
        # proxies = {'https':'http://'+userText+':'+pswText+'@proxy-xm:8080'}
        endpoint = str(os.getenv("AUTH_ENDPOINT"))
        url = str(self.base_auth_url) + endpoint
        # print(f'url: {url}')

        headers = CaseInsensitiveDict()
        headers["accept"] = "*/*"
        headers["api-version"] = "1"
        headers["Authorization"] = (
            "{validacion: 1,usuario: " + userText + ",contrasena: " + pswText + "}"
        )
        headers["Content-Type"] = "application/json"
        payload = (
            '{"validacion":1,"usuario":"'
            + userText
            + '","contrasena":"'
            + pswText
            + '"}'
        )

        try:
            if self.env == "prod":
                # r = requests.post(urlA, headers=headers, data=payload, proxies=proxies)
                response = requests.post(
                    url, headers=headers, data=payload, timeout=50
                )  ### PRODUCTIVO
            else:
                response = requests.get(
                    url, timeout=50
                )  ### -------- PRUEBAS --------------
            resp = response.json()
            # print(f"Response code: {r.status_code}");
            # print(f'Respuesta: {response}');
            if response.status_code == 200:
                self._token = json.loads(response.text)
                # print(f"Token: {self._Token['token']}");
            else:
                self._token = {"error": resp}
                print(f"Se ha presentado error {response.status_code}: {resp}")
            return self._token
        except (ConnectionError, RemoteDisconnected) as err:
            print("Se ha presentado Error: ", err)
            self._token = {"error": err}
            return self._token

    def get_data(
        self, date1, date2, selectedSource="todos", customColsReq=False
    ) -> dict:
        """Get data from the backend based on the provided date."""
        ##TODO: Implement custom columns functionality and Env variables for file DB (prod:server, dev:local file)
        if not customColsReq:
            token = self._token
            # print('Token usado: ', Token);
            # baseUrl = os.getenv("MANEUVER_URL"); ### PRODUCTIVO
            # baseUrl = f"http://localhost:{self.port}/"; ### -------- PRUEBAS --------------
            # proxies = {'https':'http://'+userText+':'+pswText+'@proxy-xm:8080'}
            endpoint = str(os.getenv("ACTIONS_ENDPOINT"))
            actionsNumber = 10000
            url = str(self.base_actions_url) + endpoint
            # print(f'url: {url}')
            headers = CaseInsensitiveDict()
            headers["accept"] = "*/*"
            headers["Content-Type"] = "application/json"
            if "token" in token.keys():
                headers = {"Authorization": "Bearer " + str(token["token"])}
                # baseUrl = os.getenv("MANEUVER_URL");
                # endpoint = os.getenv("ACTION_ENDPOINT");
                # dFec = dt.datetime.strptime(self.ui.entFecha.text(), "%Y-%m-%d")
                # dCsl = dFec.strftime('%Y-%m-%d')
                jsonPayload = {
                    "dateFrom": date1 + " 00:00",
                    "dateTo": date2 + " 23:59:00",
                    "statusIds": [],
                    "systems": [],
                    "elementIds": [],
                    "elementCompanyNames": [],
                    "elementTypeIds": [],
                    "actionTypeIds": [],
                    "originPanelIds": [],
                    "sourceCND": (
                        "true" if selectedSource in ["CND", "todos"] else "false"
                    ),
                    "sourceAgents": (
                        "true" if selectedSource in ["agentes", "todos"] else "false"
                    ),
                    "limitTo": actionsNumber,
                    "showCneZniElementDetail": "true",
                }
                # payload = json.dumps(JSONpayload);
                if self.env == "prod":
                    response = requests.post(
                        url, headers=headers, json=jsonPayload, timeout=50
                    )  ### PRODUCTIVO #json para usar json, data para usar cadena de string.
                else:
                    if selectedSource == "agentes":
                        selectedSource = "Agente"
                    params = {"source": selectedSource}
                    response = requests.get(
                        url, timeout=50, params=params
                    )  ### -------- PRUEBAS --------------
                if response.status_code == 200:
                    resp = response.json()
                else:
                    resp = {"error": f"Se ha presentado error {response.status_code}"}
                    print(f"Se ha presentado error {response.status_code}")
                # print("Atributos: ", resp[0].keys());
                # Atributos disponibles:
                # ['id', 'actionTypeId', 'actionType', 'flowId', 'flow',
                # 'flowConsecutive', 'scheduledStartDate', 'elementId', 'elementTypeId',
                # 'elementName', 'elementCompanyName', 'elementCompanyShortName', 'instructionTime',
                # 'occurrenceTime', 'confirmationTime', 'causeStatusId', 'causeStatus',
                # 'consignmentId', 'causeChangeAvailabilityId', 'causeChangeAvailability',
                # 'newAvailability', 'elementCausingId', 'causeSuspendedExecutionId',
                # 'causeSuspendedExecution', 'fileDocumentNumber', 'associatedActionId',
                # 'causeOperationalId', 'causeOperational', 'controlVQId', 'controlVQ',
                # 'teleprotectionId', 'teleprotection', 'finalElement', 'percentage',
                # 'instructionTimeChecked', 'occurrenceTimeChecked', 'confirmationTimeChecked',
                # 'order','parentTimeActionId', 'parentTypeTimeAssociatedId',
                # 'parentTypeTimeAssociated', 'typeTimeAssociatedId', 'typeTimeAssociated',
                # 'withPriorAuthorization','isVoltageControl','hidden','description',
                # 'verificationNote', 'statusTypeId', 'statusType', 'locked', 'lockedByActionId',
                # 'system', 'originPanelId', 'originPanel', 'causeOrigin', 'causeDetailCno',
                # 'additionalFieldsValue', 'dashboardOrderingDate', 'espId', 'espName',
                # 'espElementId', 'creationTime', 'filterActionOrderingDate', 'unavailableActionId',
                # 'subSystemUnavailableAction', 'cneZone', 'fuel', 'fuelName', 'fuelCEN','plantCEN',
                # 'qualityScheme', 'notification', 'reverseNotificationGenerated', 'source',
                # 'disableAvailabilityField', 'dna', 'userValidator', 'configurationId',
                # 'configurationDesc', 'thermalStateId', 'descriptionAdditional']
            else:
                # resp = json.dumps({"error": "Autenticación expirada. Vuelva a autenticarse."},
                # indent=4, sort_keys=True, ensure_ascii=False);
                resp = {"error": "Autenticación expirada. Vuelva a autenticarse."}
            # print(f'GetData response: {resp}');
        else:
            resp = {
                "error": "Funcionalidad de columnas personalizadas no implementada aún."
            }
        return resp

    def log_in(self, userEntry, pswEntry):
        """Handle user login and return the authentication status."""
        infoText = ""
        userText = userEntry.get()
        pswText = pswEntry.get()
        token = self.get_token(userText, pswText)

        if not isinstance(token, (ConnectionError, RemoteDisconnected)):
            if "error" in token.keys():
                infoText = token["error"]

                if isinstance(token["error"], (ConnectionError, RemoteDisconnected)):
                    infoText = (
                        "Error de conexión al servidor."
                        "Verifique su conexión e intente nuevamente."
                    )
                else:
                    keys = set(token["error"].keys())
                    print(token)
                    if "StatusCode" in keys:
                        error = token["error"]
                        errorMsg = error["Message"].split(".")
                        if error["StatusCode"] != 200:
                            infoText = (
                                f"Error de autenticación: {error['StatusCode']} - "
                                f"{errorMsg[0]}"
                            )
        else:
            infoText = "Error de conexión al servidor. Verifique su conexión e intente nuevamente."
        # self.getData(Token, date)
        # headers = {"Authorization": "Bearer MYREALLYLONGTOKENIGOT"}
        # text1.delete("1.0", END);
        # text1.insert(END, entryG);
        userEntry.set("")
        pswEntry.set("")
        return infoText
