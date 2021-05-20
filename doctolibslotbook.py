import requests
import json
import os
import re 

# Get total number of Pages
def getPageNumber(city):
    host = hostName + '/vaccination-covid-19/'+city+'?ref_visit_motive_ids%5B%5D='+str(visitMotifID1)+'&ref_visit_motive_ids%5B%5D='+str(visitMotifID2)
    response = requests.get(host)
    apiResponse = response.text

    match_list = []
    regex = 'search_results_total&quot;:\d+'
    match_list = re.findall(regex, apiResponse)
    splitPattern = match_list[0].split(':')
    totalPages = int(int(splitPattern[1])/10)
    print('Total Pages: '+str(totalPages))
    return(totalPages)


# Get center IDs per page
def fetCenterId(pageNumber, city):
    if (pageNumber == 1):
        host = hostName + '/vaccination-covid-19/'+city+'?ref_visit_motive_ids%5B%5D='+str(visitMotifID1)+'&ref_visit_motive_ids%5B%5D='+str(visitMotifID2)
    else:
        host = hostName+'/vaccination-covid-19/'+city+'?page='+str(pageNumber)+'&ref_visit_motive_ids%5B%5D='+str(visitMotifID1)+'&ref_visit_motive_ids%5B%5D='+str(visitMotifID2)

    response = requests.get(host)
    apiResponse = response.text
    regex = 'id="search-result-\d+'
    match_list = re.findall(regex, apiResponse)

    centerIds = []
    for i in match_list:
        splitPattern = i.split('-')
        centerIds.append(splitPattern[2])

    return(centerIds)


# Request Availability by Center ID
def requestAvailabilityByCenterID(centerId):
    host = hostName + '/search_results/'+str(centerId)+'.json?ref_visit_motive_ids%5B%5D='+str(visitMotifID1)+'&ref_visit_motive_ids%5B%5D='+str(visitMotifID2)+'&speciality_id='+str(specialityID)+'&search_result_format=json&force_max_limit=2'
    response = requests.get(host)
    apiResponse = response.text
    apiResponse = json.loads(apiResponse)
    return checkAvailability(apiResponse, host)

# Check for Availability
def checkAvailability(apiResponse, host):
    if len(apiResponse["availabilities"]) > 0:
        print('Slots available: ', apiResponse["total"])
        print('City: ', apiResponse["search_result"]["city"])
        print('Center: ', apiResponse["search_result"]["name_with_title"])
        print('Appointment available on : '+hostName+apiResponse["search_result"]["link"])
    else:
        print('No slots available in: ', apiResponse["search_result"]["name_with_title"])


# Main function
if __name__ == "__main__":
    visitMotifID1 = 6970
    visitMotifID2 = 7005
    specialityID = 5494
    hostName = 'https://www.doctolib.fr'

    city = input('What is your city? (should be written like this : nogent-sur-marne) ')

    host = hostName+'/vaccination-covid-19/'+city+'?ref_visit_motive_ids%5B%5D='+str(visitMotifID1)+'&ref_visit_motive_ids%5B%5D='+str(visitMotifID2)
    print(host)

    totalPages = getPageNumber(city)
    # pageNumber = 2
    for pageNumber in range(1, totalPages):
        centerIds = fetCenterId(pageNumber, city)
        for centerId in centerIds:
            requestAvailabilityByCenterID(centerId)
