class SpiderJob:
    def __init__(self, spider_id, job_id, status):
        self.spider_id = spider_id
        self.job_id = job_id
        self.status = status


class Student:
    def __init__(self, id, name, sex, age):
        self.id = id
        self.name = name
        self.sex = sex
        self.age = age

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_sex(self):
        return self.sex

    def get_age(self):
        return self.age

    def set_id(self, id):
        self.id = id

    def set_name(self, name):
        self.name = name

    def set_sex(self, sex):
        self.sex = sex

    def set_age(self, age):
        self.age = age

    def msg(self):
        return '{id: %s;name: %s;sex: %s;age: %s' % (self.id, self.name, self.sex, self.age)
