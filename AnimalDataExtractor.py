import requests
import json
from os.path import isfile, join, exists
from os import listdir
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

    def downloadAllAnimals(self, override):
        animalList = self.getAnimalList(override)
        #  #sprint('animal list: {0}'.format(animalList))

        # FOR LOOP: go through the animalList and extract all the IDs,
        # then use each of them to get the info for each of them
        count = 1

        for animalInfo in animalList:
            animalId = animalInfo['_id']
            print(f'Saving animal {count}: {animalId}')
            self.downloadSingleAnimal(animalId, override)
            count += 1

    def downloadSingleAnimal(self, animalId, override):
        animalDetails = self.getAnimalDetails(animalId)
        if override or not exists(f'./animal_data/animal_details/{animalId}.json'):
            self._saveAnimalToFile(animalDetails, animalId)

    def getAnimalsDocumentData(self):
        animalList = self._getDownloadedAnimalIds()
        animalDocumentDataResult = []

        for animalId in animalList:
            animalDetails = self._getAnimalFromFile(animalId)
            animalDocumentData = self._detailsToDocumentData(
                animalDetails, animalId)
            animalDocumentDataResult += [animalDocumentData]

        return animalDocumentDataResult
    
    def _getDownloadedAnimalIds(self):
        detailsPath = './animal_data/animal_details/' 
        return [f[:24] for f in listdir(detailsPath) if isfile(join(detailsPath, f))]

    def _detailsToDocumentData(self, animalDetails, catalogId):
        animalDocumentData = AnimalDocumentData()
        animalDocumentData.summary = ''
        if 'behaviorApprovedInUse' in animalDetails.keys():
            animalDocumentData.behaviour = animalDetails[
                'behaviorApprovedInUse'][
                    'behavior']['behaviorUnstructured']

        animalDocumentData.catalogId = catalogId

        if 'commonNames' in animalDetails.keys():
            animalDocumentData.commonNames = self._getCommonNames(
                animalDetails['commonNames'])
        else:
            commonNames = self._initCommonNames()
            commonNames['general'] = [animalDetails['scientificNameSimple']]
            animalDocumentData.commonNames = commonNames

        if 'threatStatusApprovedInUse' in animalDetails.keys():
                animalDocumentData.endangeredStatus = self._getEndangeredStatus(
                    animalDetails[
                        'threatStatusApprovedInUse'][
                            'threatStatus'])
            
        if 'feedingApprovedInUse' in animalDetails.keys():
            animalDocumentData.feeding = animalDetails['feedingApprovedInUse'][
                'feeding']['feedingUnstructured']

        if 'fullDescriptionApprovedInUse' in animalDetails.keys():
            animalDocumentData.fullDescription = animalDetails[
                'fullDescriptionApprovedInUse']['fullDescription'][
                    'fullDescriptionUnstructured']

        if 'abstractApprovedInUse' in animalDetails.keys():
            animalDocumentData.generalDescription = animalDetails[
                'abstractApprovedInUse']['abstract']

        if 'habitatsApprovedInUse' in animalDetails.keys():
            animalDocumentData.habitat = animalDetails['habitatsApprovedInUse'][
                'habitats']['habitatUnstructured']

        if 'ancillaryDataApprovedInUse' in animalDetails.keys():
            animalDocumentData.imagesLocation = self._getImagesLocation(
                animalDetails['ancillaryDataApprovedInUse']['ancillaryData'])
        
        if 'lifeCycleApprovedInUse' in animalDetails.keys():
            animalDocumentData.lifeCycle = animalDetails[
                'lifeCycleApprovedInUse'][
                    'lifeCycle']['lifeCycleUnstructured']
        
        if 'lifeFormApprovedInUse' in animalDetails.keys():
            animalDocumentData.lifeForm = animalDetails[
                'lifeFormApprovedInUse'][
                    'lifeForm']['lifeFormUnstructured']
        
        if 'migratoryApprovedInUse' in animalDetails.keys():
            animalDocumentData.migration = animalDetails[
                'migratoryApprovedInUse'][
                    'migratory']['migratoryUnstructured']
        
        if 'reproductionApprovedInUse' in animalDetails.keys():
            animalDocumentData.reproduction = animalDetails[
                'reproductionApprovedInUse']['reproduction'][
                    'reproductionUnstructured']

        if 'scientificNameSimple' in animalDetails.keys():
            animalDocumentData.scientificName = animalDetails['scientificNameSimple']

        return animalDocumentData

    def _getImagesLocation(self, imagesInfo):
        imagesLocation = []
        for image in imagesInfo:
            if image['source'] or image['mediaURL']:
                if image['source'] and image['source'] not in imagesLocation:
                    imagesLocation += [image['source']]
                for mediaImage in image['mediaURL']:
                    if mediaImage not in imagesLocation:
                        imagesLocation += [mediaImage]
        return imagesLocation

    def _getEndangeredStatus(self, endangeredStatusRaw):
        endangeredStatusResult = {}
        for endangeredStatus in endangeredStatusRaw:
            if endangeredStatus['threatStatusAtomized']['appliesTo'][
                    'country'] == COLOMBIA:
                try:
                    endangeredStatusResult['colombia'] = endangeredStatus[
                        'threatStatusAtomized']['threatCategory'][
                            'measurementValue']
                except KeyError as e:
                    print('No endangered status for Colombia found')
            elif endangeredStatus['threatStatusAtomized']['appliesTo'][
                    'country'] == GLOBAL:
                try:
                    endangeredStatusResult['global'] = endangeredStatus[
                        'threatStatusAtomized']['threatCategory'][
                            'measurementValue']
                except KeyError as e:
                    print('No endangered status for Global found')
        return endangeredStatusResult

    def _getCommonNames(self, commonNames):
        commonNamesResult = self._initCommonNames()
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
    
    def _initCommonNames(self):
        commonNames = {}
        commonNames['general'] = []
        commonNames['spanish'] = []
        commonNames['english'] = []
        return commonNames

    def _saveAnimalToFile(self, animalDetails, animalId):
        jsonString = json.dumps(animalDetails, indent=4, sort_keys=True)
        with open(f'./animal_data/animal_details/{animalId}.json', 'w') as text_file:
            print(jsonString, file=text_file)
    
    def _getAnimalFromFile(self, animalId):
        with open(f'./animal_data/animal_details/{animalId}.json') as json_file:
            return json.load(json_file)

    def downloadAnimalList(self):
        countAnimalsParams = {
            'count': 'true',
            'kingdom': self.kingdom,
            'department': self.department
        }

        # mocking value to avoid data consumption
        countAnimalsResponse = requests.get(self.countAnimalsUrl,
                                            params=countAnimalsParams)
        animalNumber = countAnimalsResponse.json()['total']
        # animalNumber = 1
        print(f'Number of animals: {animalNumber}')

        animalListParams = {
            'kingdom': self.kingdom,
            'department': self.department,
            'size': animalNumber
        }
        animalListResponse = requests.get(self.animalListUrl,
                                          params=animalListParams)
        jsonString = json.dumps(
            animalListResponse.json(), indent=4, sort_keys=True)
        with open('./animal_data/animal_list.json', 'w') as text_file:
            print(jsonString, file=text_file)

    def getAnimalList(self, override):
        if override or not exists('./animal_data/animal_list.json'):
            self.downloadAnimalList()

        with open('./animal_data/animal_list.json') as json_file:
            return json.load(json_file)

    def getAnimalDetails(self, animalId):
        animalDetailsUrl = (
            'http://api.catalogo.biodiversidad.co'
            '/api/v1.5/complete-record/') + str(
            animalId)
        animalDetailsResponse = requests.get(animalDetailsUrl)
        return animalDetailsResponse.json()
