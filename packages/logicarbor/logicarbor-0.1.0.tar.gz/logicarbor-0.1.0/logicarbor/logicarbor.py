import requests


class API:
    def __init__(self, token):
        self.api_key = token
        self.base_url = "https://api.logicarbor.com/v3.0"

    def checkUser(self, userId):
        url = f"{self.base_url}/?mode=check&user_id={userId}&key={self.api_key}"
        response = requests.get(url)
        return response.text

    def editUser(self, userId, userName="", endDate=""):
        url = f"{self.base_url}/?mode=edit&user_id={userId}&key={self.api_key}&user_name={userName}&end_date={endDate}"
        response = requests.get(url)
        return response.text

    def addUser(self, userName, endDate=""):
        url = f"{self.base_url}/?mode=add&key={self.api_key}&user_name={userName}&end_date={endDate}"
        response = requests.get(url)
        return response.text

    def enableUser(self, userId):
        url = f"{self.base_url}/?mode=enable&key={self.api_key}&user_id={userId}"
        response = requests.get(url)
        return response.text

    def disableUser(self, userId):
        url = f"{self.base_url}/?mode=disable&key={self.api_key}&user_id={userId}"
        response = requests.get(url)
        return response.text

    def deleteUser(self, userId):
        url = f"{self.base_url}/?mode=delete&key={self.api_key}&user_id={userId}"
        response = requests.get(url)
        return response.text
