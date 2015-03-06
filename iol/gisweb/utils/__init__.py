from zope.i18nmessageid import MessageFactory
from AccessControl import allow_module
allow_module('iol.gisweb.utils.interfaces')
allow_module('iol.gisweb.utils.IolDocument')
MessageFactory = MessageFactory('iol.gisweb.utils')

from DateTime import DateTime
import simplejson as json

class dateEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,DateTime):
            return obj.strftime("%d/%m/%Y")
        return json.JSONEncoder.default(self,obj)