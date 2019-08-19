from AnimalDataExtractor import AnimalDataExtractor
from AnimalDataExporter import AnimalDataExporter


def main():
    animalDataExtractor = AnimalDataExtractor()
    animalDataExporter = AnimalDataExporter()
    # override = False
    # animalDataExtractor.downloadAnimalList()
    # animalDataExtractor.downloadAllAnimals(override)
    # animalDataExtractor.downloadSingleAnimal(
    #     '592d8ef6f827bf0c0cede227', override)
    animalDataExporter.exportData(animalDataExtractor.getAnimalsDocumentData())
    # animalDataExporter._getImageUrl('')

if __name__ == "__main__":
    main()
