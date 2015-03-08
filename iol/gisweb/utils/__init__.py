from zope.i18nmessageid import MessageFactory
from AccessControl import allow_module
from DateTime import DateTime
import simplejson as json
import os

allow_module('iol.gisweb.utils.interfaces')
allow_module('iol.gisweb.utils.IolDocument')
MessageFactory = MessageFactory('iol.gisweb.utils')

class dateEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,DateTime):
            return obj.strftime("%d/%m/%Y")
        return json.JSONEncoder.default(self,obj)

class loadJsonFile(object):
    def __init__(self, file):
        self.file = file
    def __call__(self):
        if not os.path.isfile(self.file):
            return dict()
        with open(self.file) as json_data:
            try:
                d = json.loads(json_data)
            except:
                return dict()
            return d