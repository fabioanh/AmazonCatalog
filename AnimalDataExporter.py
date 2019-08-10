import jinja2
from AnimalDocumentData import AnimalDocumentData


class AnimalDataExporter:

    def exportData(self, animalDocumentDataList):
        templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "index.html"
        TEMPLATE_FILE_ARTICLE = "article_content"
        template = templateEnv.get_template(TEMPLATE_FILE_ARTICLE)
        articlesText = ''
        for animalDocumentData in animalDocumentDataList:
            articlesText += template.render(document=animalDocumentData)
        template = templateEnv.get_template(TEMPLATE_FILE)
        html_file = open('./templates/AmazonCatalogOutput.html', 'w')
        articlesHtml = template.render(articlesContent=articlesText)
        html_file.write(articlesHtml)
        html_file.close()
