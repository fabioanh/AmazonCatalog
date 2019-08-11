import requests
import json
from AnimalDocumentData import AnimalDocumentData

COLOMBIA = 'Colombia'
GLOBAL = 'Global'
ENGLISH_LANGUAGE = 'Inglés'
SPANISH_LANGUAGE = 'Español'


class AnimalDataExtractor:
    department = 'CO-AMA'
    kingdom = 'animalia'
    countAnimalsUrl = (
        'http://api.catalogo.biodiversidad.co'
        '/api/v1.5/record_search/advanced_search')
    animalListUrl = (
        'http://api.catalogo.biodiversidad.co'
        '/api/v1.5/record_search/advanced_search')

    def extractData(self):
        animalList = self.getAnimalList()
        #  #sprint('animal list: {0}'.format(animalList))
        animalDocumentDataResult = []

        # FOR LOOP: go through the animalList and extract all the IDs,
        # then use each of them to get the info for each of them

        for animalInfo in animalList:
            animalId = animalInfo['_id']
            if 'threatStatusApprovedInUse' in animalInfo.keys():
                endangeredStatus = animalInfo['threatStatusApprovedInUse'][
                    'threatStatus']
            summary = animalInfo['fullDescriptionApprovedInUse'][
                'fullDescription']['fullDescriptionUnstructured']
            animalDetails = self.getAnimalDetails(animalId)
            # self.saveDataToFile(animalDetails, animalId)
            # #print('animalId: {0}'.format(animalInfo['_id']))
            animalDocumentData = self.detailsToDocumentData(
                animalDetails, summary, endangeredStatus, animalId)
            animalDocumentDataResult += [animalDocumentData]
            # print(animalDocumentData)
        return animalDocumentDataResult

    def detailsToDocumentData(self, animalDetails, summary, endangeredStatus,
                              catalogId):
        animalDocumentData = AnimalDocumentData()
        animalDocumentData.summary = summary
        animalDocumentData.behaviour = animalDetails['behaviorApprovedInUse'][
            'behavior']['behaviorUnstructured']
        animalDocumentData.catalogId = catalogId
        animalDocumentData.commonNames = self._getCommoonNames(
            animalDetails['commonNames'])
        animalDocumentData.endangeredStatus = self._getEndangeredStatus(
            endangeredStatus)
        animalDocumentData.feeding = animalDetails['feedingApprovedInUse'][
            'feeding']['feedingUnstructured']
        animalDocumentData.fullDescription = animalDetails[
            'fullDescriptionApprovedInUse']['fullDescription'][
                'fullDescriptionUnstructured']
        animalDocumentData.generalDescription = animalDetails[
            'abstractApprovedInUse']['abstract']
        animalDocumentData.habitat = animalDetails['habitatsApprovedInUse'][
            'habitats']['habitatUnstructured']
        animalDocumentData.imagesLocation = self._getImagesLocation(
            animalDetails['ancillaryDataApprovedInUse']['ancillaryData'])
        animalDocumentData.lifeCycle = animalDetails['lifeCycleApprovedInUse'][
            'lifeCycle']['lifeCycleUnstructured']
        animalDocumentData.lifeForm = animalDetails['lifeFormApprovedInUse'][
            'lifeForm']['lifeFormUnstructured']
        animalDocumentData.migration = animalDetails['migratoryApprovedInUse'][
            'migratory']['migratoryUnstructured']
        animalDocumentData.reproduction = animalDetails[
            'reproductionApprovedInUse']['reproduction'][
                'reproductionUnstructured']
        return animalDocumentData

    def _getImagesLocation(self, imagesInfo):
        imagesLocation = []
        for image in imagesInfo:
            if image['source'] and image['mediaURL']:
                if image['source'] not in imagesLocation:
                    imagesLocation += [image['source']]
        return imagesLocation

    def _getEndangeredStatus(self, endangeredStatusRaw):
        endangeredStatusResult = {}
        for endangeredStatus in endangeredStatusRaw:
            if endangeredStatus['threatStatusAtomized']['appliesTo'][
                    'country'] == COLOMBIA:
                endangeredStatusResult['colombia'] = endangeredStatus[
                    'threatStatusAtomized']['threatCategory'][
                        'measurementValue']
            elif endangeredStatus['threatStatusAtomized']['appliesTo'][
                    'country'] == GLOBAL:
                endangeredStatusResult['global'] = endangeredStatus[
                    'threatStatusAtomized']['threatCategory'][
                        'measurementValue']
        return endangeredStatusResult

    def _getCommoonNames(self, commonNames):
        commonNamesResult = {}
        commonNamesResult['general'] = []
        commonNamesResult['spanish'] = []
        commonNamesResult['english'] = []

        for commonName in commonNames:
            if 'language' not in commonName.keys():
                commonNamesResult['general'] += [str(commonName['name'])]
            elif commonName['language'] == SPANISH_LANGUAGE:
                commonNamesResult['spanish'] += [str(commonName['name'])]
            elif commonName['language'] == ENGLISH_LANGUAGE:
                commonNamesResult['english'] += [str(commonName['name'])]
        if not commonNamesResult['general']:
            commonNamesResult['general'] = commonNamesResult['spanish'][:3]
        return commonNamesResult

    def saveDataToFile(self, animalDetails, animalId):
        jsonString = json.dumps(animalDetails, indent=4)
        with open(f'./animal_details/{animalId}.json', 'w') as text_file:
            print(jsonString, file=text_file)

    def getAnimalList(self):
        # countAnimalsParams = {
        #     'count': 'true',
        #     'kingdom': self.kingdom,
        #     'department': self.department
        # }

        # # mocking value to avoid data consumption
        # countAnimalsResponse = requests.get(self.countAnimalsUrl,
        #                                     params=countAnimalsParams)
        # animalNumber = countAnimalsResponse.json()['total']
        # #print('Number of animals: {0}'.format(animalNumber))
        animalNumber = 8

        animalListParams = {
            'kingdom': self.kingdom,
            'department': self.department,
            'size': animalNumber
        }
        animalListResponse = requests.get(self.animalListUrl,
                                          params=animalListParams)
        return animalListResponse.json()

    def getAnimalDetails(self, animalId):
        animalDetailsUrl = (
            'http://api.catalogo.biodiversidad.co'
            '/api/v1.5/complete-record/') + str(
            animalId)
        animalDetailsResponse = requests.get(animalDetailsUrl)
        return animalDetailsResponse.json()
