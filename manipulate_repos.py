import requests
import base64
import os
from dotenv import load_dotenv

class ManipulateRepos:

    def __init__(self, username):
        load_dotenv()
        api_token_github = f'Bearer {os.getenv('API_TOKEN_GITHUB')}'
        
        self.username = username
        self.api_base_url = "https://api.github.com"
        self.headers = {
            "X-Github-Api-Version": "2022-11-28",
            "Authorization": api_token_github,
            "Accept": "application/vnd.github+json",
        }

    def __repo_exists(self, repo_name):

        try:
            response = requests.get(
                f"{self.api_base_url}/repos/{self.username}/{repo_name}"
            )

            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                return False
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Error", e)

    def create_repo(self, repo_name):

        repo_exists = self.__repo_exists(repo_name)

        data = {
            "name": repo_name,
            "description": f"Dados dos repositórios de {repo_name}.",
            "private": True,
        }

        if not repo_exists:

            try:
                response = requests.post(
                    f"{self.api_base_url}/user/repos", json=data, headers=self.headers
                )
                response.raise_for_status()
                print(f"create repo status_code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print("Error", e)
        else:
            print("Repositório já existe!")

    def encoded_file(self, file_name):

        with open(f"./data/{file_name}", "rb") as file:
            file_content = file.read()
            encoded_content = base64.b64encode(file_content)

        return encoded_content

    def add_file(self, repo_name, file_name):

        file_encoded = self.encoded_file(file_name)

        data = {
            "message": "Adicionando um novo arquivo.",
            "content": file_encoded.decode("utf-8"),
        }

        try:
            response = requests.put(
                f"{self.api_base_url}/repos/{self.username}/{repo_name}/contents/{file_name}",
                headers=self.headers,
                json=data,
            )

            response.raise_for_status()
            print(f"status_code upload do arquivo: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print("Error", e)


if __name__ == "__main__":

    novo_repo = ManipulateRepos("florenncio")
    nome_repo = "linguagens-repositorios-empresas"
    novo_repo.add_file(nome_repo, "amzn.csv")
