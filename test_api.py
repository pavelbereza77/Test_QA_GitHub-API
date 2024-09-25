import json
import unittest
import logging
import requests

from environs import Env

env = Env()
env.read_env()
GITHUB_TOKEN = env('GITHUB_TOKEN')
GITHUB_USERNAME = env('GITHUB_USERNAME')
NAME_REPO = env('NAME_REPO')

url_get_list_repo = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
url_create_repo = "https://api.github.com/user/repos"
url_delete_repo = f"https://api.github.com/repos/{GITHUB_USERNAME}/{NAME_REPO}"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": 'application/vnd.github.v3+json',
    'Cache-Control': 'no-cache',
    "Pragma": "no-cache"
}

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GitHabApiTest(unittest.TestCase):

    def test_post_get_delete_repos(self):
        response_post = post_repos()
        self.assertEqual(response_post.status_code, 201)

        response_get = get_list_repos()
        self.assertEqual(response_get.status_code, 200)
        list_repos = response_get.json()
        add_repo = ' '.join(
            [list_repos[i]['name']
             for i in range(len(list_repos))
             if list_repos[i]['name'] == NAME_REPO])
        self.assertEqual(add_repo, NAME_REPO)

        response_delete = delete_repo()
        self.assertEqual(response_delete.status_code, 204)
        response_get_after = get_list_repos()
        list_repos_after = response_get_after.json()
        repos = [list_repos_after[i]['name'] for i in range(len(list_repos_after))]
        self.assertFalse(NAME_REPO in repos)


def post_repos():
    return requests.post(url=url_create_repo,
                         data=json.dumps({'name': NAME_REPO}),
                         auth=(GITHUB_USERNAME, GITHUB_TOKEN),
                         headers={"Content-Type": "application/json"})


def get_list_repos():
    return requests.get(url=url_get_list_repo, headers=headers)


def delete_repo():
    return requests.delete(url=url_delete_repo, headers=headers)
