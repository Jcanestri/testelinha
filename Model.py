class Model:
    def __init__(self, modelImage):
        self.image = modelImage

        # if we want params like the size of the field, the pixels of the lines or ...
        self.params = dict([('upperLineY', 250), ('lowerLineY', 525)])
        #self.params = dict([('upperLineY', 170), ('lowerLineY', 350)])
        #self.params = dict([('upperLineY', 125), ('lowerLineY', 265)])
        #self.params = dict([('upperLineY', 145), ('lowerLineY', 310)])
