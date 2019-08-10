from AnimalDataExtractor import AnimalDataExtractor
from AnimalDataExporter import AnimalDataExporter

def main():
    animalDataExtractor = AnimalDataExtractor()
    animalDataExporter = AnimalDataExporter()
    animalDataExporter.exportData(animalDataExtractor.extractData())

if __name__ == "__main__":
    main()
