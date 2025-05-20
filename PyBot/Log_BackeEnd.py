import requests;

class logging():

    def __init__(self):
        print("Instance Created")

    def logIn(self, userEntry, pswEntry):
        baseUrl = "https://pokeapi.co/api/v2/";
        #data = {"ip": "1.1.2.3"}
        endpoint ="pokemon/ditto"
        url = baseUrl+endpoint;
        #headers = {"Authorization": "Bearer MYREALLYLONGTOKENIGOT"}
        userText = userEntry.get();
        pswText = pswEntry.get();
        print("Usuario: ", userText);
        print("Contraseña: ", pswText);
        # text1.delete("1.0", END);
        # text1.insert(END, entryG);
        # text2.delete("1.0", END);
        # text2.insert(END, entryP);
        # text3.delete("1.0", END);
        # text3.insert(END, entryO);

        #response = requests.post(endpoint, data=data, headers=headers)
        response = requests.get(url);
        jsonResponse = response.json();
        nombre = jsonResponse["name"];
        print(f"Pokemon: {nombre}");

        userEntry.set("");
        pswEntry.set("");