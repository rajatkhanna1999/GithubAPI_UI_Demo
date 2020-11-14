import io
from base64 import b64encode
import eel
import socket
from struct import *
import datetime
import sys
import requests
import logging

maxResultsPerPage = 100
eel.init('web')

'''
	* Fetches top (topContributersCount) Contributors of a repository of a organisation (organisationName)
'''
def getTopContributers(organisationName, repository, topContributersCount):
    contributers = []
    URL = 'https://api.github.com/repos/{orgName}/{repoName}/contributors'.format(orgName = organisationName, repoName = repository)
    parameters = {
		'page': 1,
        'per_page': min(maxResultsPerPage, topContributersCount)
    }
    while(topContributersCount > 0):
        response = requests.get(url = URL, params = parameters)
        data = response.json()
        if (response.status_code == 200):
            for users in data:
                contributers.append((users['login'], users['contributions'], users['html_url']))

            if (len(data) < maxResultsPerPage):
                break
            else:
                parameters['page'] += 1
                parameters['per_page'] = min(maxResultsPerPage, topContributersCount)
                topContributersCount -= len(data)

        else:
            eel.addText(response.text, response.status_code)
            exit(1)

    return contributers

'''
	* Fetches Top (topRepositoriesCount) Repositories of (organisationName) Organisation
'''
def fetchTopRepositories(organisationName, topRepositoriesCount):
    repositories = []
    URL = 'https://api.github.com/orgs/{orgName}/repos'.format(orgName = organisationName)
    parameters = {
		'page': 1,
        'per_page': maxResultsPerPage
    }
    while(1):
        response = requests.get(url = URL, params = parameters)
        data = response.json()
        if (response.status_code == 200):
            for repos in data:
                repositories.append((repos['forks_count'], repos['name'], repos['description'], repos['html_url']))

            if (len(data) < maxResultsPerPage):
                break
            else:
                parameters['page'] += 1

        else:
            eel.addText(response.text, response.status_code)
            exit(1)

    repositories.sort(key = lambda x: x[0], reverse = True)
    return repositories[:topRepositoriesCount]

'''
	* Function called by main.js to fetch top repositories and contributors from an organisation
'''
@eel.expose
def fetchReposOfOrganisationsAndContibutors(organisationName, topRepositoriesCount, topContributersCount):
    print("Fetching Results, Plz wait!!")
    eel.addWaitMsg()
    repositories = []
    contributers = []
    toprepositories = fetchTopRepositories(organisationName, topRepositoriesCount)
    for repo in toprepositories:
        print(repo[1])
        topcontributer = getTopContributers(organisationName, repo[1], topContributersCount)
        contribution = []
        for contirbut in topcontributer:
            contribution.append(contirbut)
        
        repositories.append(repo)
        contributers.append(contribution)
    
    eel.removeWaitMsg()
    return repositories, contributers


eel.start('index.html', size=(1000, 600))
