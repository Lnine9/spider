class Industry:
    id = ''
    value = ''
    include = []
    no_include = []
    nextIndustry = None

    def __init__(self, id, value, include, no_include):
        self.id = id
        self.value = value
        if include is not None:
            self.include = include.split("\\")
        if no_include is not None:
            self.no_include = no_include.split("\\")

    #  责任链调用 划分行业
    def analysis(self, name):
        if name is None:
            return None
        for item in self.no_include:
            if item in name:
                return []+([] if self.nextIndustry is None else self.nextIndustry.analysis(name))
        for i in self.include:
            if i in name:
                return [{'id': self.id, 'name': self.value}]+([] if self.nextIndustry is None else self.nextIndustry.analysis(name))
        return []+([] if self.nextIndustry is None else self.nextIndustry.analysis(name))

    def NextIndustry(self, res):
        self.nextIndustry = res
