import requests
import pandas as pd
import re
import os
from dotenv import load_dotenv

class DataRepositories:

    def __init__(self, owner):
        load_dotenv()
        api_token_github = f'Bearer {os.getenv('API_TOKEN_GITHUB')}'
        
        self.owner = owner
        self.api_url_base = "https://api.github.com"
        self.headers = {
            "X-Github-Api-Version": "2022-11-28",
            "Authorization": api_token_github,
            "Accept": "application/vnd.github+json",
        }

    def __fetch_repos(self):

        url = f"{self.api_url_base}/users/{self.owner}/repos"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print("Error", e)
            return None

        return response

    def get_repos_list(self):

        repos_list = []
        response = self.__fetch_repos()
        link_header = response.headers.get("Link", None)

        if link_header:

            match = re.search(r'page=(\d+)>;\s*rel="last"', link_header)
            num_page = int(match.group(1))

            for page_num in range(1, num_page):
                try:
                    url_page = (
                        f"{self.api_url_base}/users/{self.owner}/repos?page={page_num}"
                    )
                    response = requests.get(url_page, headers=self.headers)
                    repos_list.append(response.json())
                except:
                    repos_list.append(None)

        return repos_list

    def names_repos(self):

        repos_list = self.get_repos_list()
        repos_names = []

        for page in repos_list:
            for repo in page:
                try:
                    repos_names.append(repo["name"])
                except:
                    pass

        return repos_names

    def names_languages(self):

        repos_list = self.get_repos_list()
        repos_languages = []

        for page in repos_list:
            for repo in page:
                try:
                    repos_languages.append(repo["language"])
                except:
                    pass
        return repos_languages

    def create_df_language(self):

        names = self.names_repos()
        language = self.names_languages()

        df = pd.DataFrame()
        df["repository_name"] = names
        df["language"] = language

        return df

    def save_df_language(self, df):

        df.to_csv(f"./data/{self.owner}.csv")
        print("Arquivo salvo!")


if __name__ == "__main__":

    amazon_repo = DataRepositories("amzn")
    df_lang_amnz = amazon_repo.create_df_language()
    amazon_repo.save_df_language(df_lang_amnz)
