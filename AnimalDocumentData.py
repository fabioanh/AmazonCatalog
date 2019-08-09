class AnimalDocumentData:
    behaviour = ''
    catalogId = ''
    commonNames = {}  #grouped by languagge
    endangeredStatus = {}  #Colombian one and global one
    feeding = ''
    fullDescription = ''
    generalDescription = ''
    habitat = ''
    imagesLocation = []
    lifeCycle = ''
    lifeForm = ''
    migration = ''
    reproduction = ''
    summary = ''

    def __str__(self):
        return f'behaviour: {self.behaviour}, \ncatalog id: {self.catalogId}, \ncommon names: {self.commonNames}, \nendangered status: {self.endangeredStatus}, \nfeeding: {self.feeding}, \nfull description: {self.fullDescription}, \ngeneral description: {self.generalDescription}, \nhabitat: {self.habitat}, \nimages: {self.imagesLocation}, \nlife cycle: {self.lifeCycle}, \nlife form: {self.lifeForm}, \nmigration: {self.migration}, \nreproduction: {self.reproduction}, \nsummary: {self.summary}'
