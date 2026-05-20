import requests
from requests.exceptions import (
    RequestException,
    ConnectionError,
    Timeout,
    HTTPError,
    TooManyRedirects,
    URLRequired,
)
from prompt_toolkit import prompt
import actionAnswers

def get_username_request(username):
    headers = {'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2026-03-10'}
    
    link = f'https://api.github.com/users/{username}/events'
    #link = f'https://api.github.com/users/{username}/events?per_page=100' # --> cambia la cantidad de elementos por página
    response = requests.get(link,headers=headers,timeout=5)
    return response

def response_to_dictonary(response):
    response_list = response.json()
    events = []
    for response_dict in response_list:
        eventType = response_dict["type"]
        repoName = response_dict["repo"]["name"]
        events += [[eventType,repoName]]

    repositoriesDictionary = {}
    for event in events:
        repoKey = event[1]
        eventType = event[0]
        if repoKey in repositoriesDictionary:
            if eventType in repositoriesDictionary[repoKey]:
                repositoriesDictionary[repoKey][eventType] += 1
            else:
                repositoriesDictionary[repoKey][eventType] =  1

        else:
            repositoriesDictionary[repoKey] = {eventType: 1}
    return repositoriesDictionary

def display_activity(repositoriesDictionary):
    if len(repositoriesDictionary) > 0:
        for repo in repositoriesDictionary:
            repoDictionary = repositoriesDictionary[repo]
            for action in repoDictionary:
                text = actionAnswers.messageToDisplay[action]
                count = repoDictionary[action]
                print(text % (count, repo))
    else:
        print("No activity to show.")

if __name__ == '__main__':
    username = prompt("Enter GitHub username to view activity: ")
    try:
        response = get_username_request(username)
        response.raise_for_status()
        repositoriesDictionary = response_to_dictonary(response)
        display_activity(repositoriesDictionary)
    except ConnectionError:
        print("Cannot connect to server")
    except requests.HTTPError as e:
        status = e.response.status_code  
        print(f"Server Error: {status}")
    except Timeout:
        print("Request exceeded timeout limit.")
    except TooManyRedirects:
        print("Too many redirects")
    except RequestException as e:
        print(f"Unexpected error: {e}")

    
