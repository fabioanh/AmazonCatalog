import jinja2
from AnimalDocumentData import AnimalDocumentData


class AnimalDataExporter:

    def exportData(self, animalDocumentDataList):
        templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "index.html"
        template = templateEnv.get_template(TEMPLATE_FILE)
        outputText = template.render()
        html_file = open('./templates/AmazonCatalogOutput.html', 'w')
        for animalDocumentData in animalDocumentDataList:
            html_file.write(outputText)
        html_file.close()
