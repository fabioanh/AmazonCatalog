class AnimalDocumentData:
    behaviour = ''
    catalogId = ''
    commonNames = {}  # grouped by languagge
    endangeredStatus = {}  # Colombian one and global one
    feeding = ''
    fullDescription = ''
    generalDescription = ''
    habitat = ''
    imagesLocation = []
    lifeCycle = ''
    lifeForm = ''
    migration = ''
    reproduction = ''
    scientificName = ''
    summary = ''

    def __str__(self):
        return f(
            'behaviour: {self.behaviour}, \n'
            'catalog id: {self.catalogId}, \n'
            'common names: {self.commonNames}, \n'
            'endangered status: {self.endangeredStatus}, \n'
            'feeding: {self.feeding}, \n'
            'full description: {self.fullDescription}, \n'
            'general description: {self.generalDescription}, \n'
            'habitat: {self.habitat}, \n'
            'images: {self.imagesLocation}, \n'
            'life cycle: {self.lifeCycle}, \n'
            'life form: {self.lifeForm}, \n'
            'migration: {self.migration}, \n'
            'reproduction: {self.reproduction}, \n'
            'scientific name: {self.scientificName}, \n'
            'summary: {self.summary}')
