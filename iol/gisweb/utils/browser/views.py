from plone import api
from ..IolDocument import IolDocument
from Products.CMFPlone.utils import getToolByName



# Get Iol Role on Object
class getIolRoles(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        doc = self.aq_parent
        iDoc = IolDocument(doc)
        return iDoc.getIolRoles(doc)

# Retrieve Objects's WorkFlow Info
class wfInfo(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        doc = self.aq_parent
        iDoc = IolDocument(doc)
        self.request.response.headers['Content-Type'] = 'application/json'
        return iDoc.wfInfo()



# Get Workflow State
class getState(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        doc = self.aq_parent
        return api.content.get_state(obj=doc)

# List of all available Transition
class getTransitions(object):

    def __init__(self,context,request):
        self.context = context
        self.request = request

    def __call__(self):
        return ""


class nextNumber(object):

    def __init__(self,context,request):
        self.context = context
        self.request = request

    def __call__(self,field='numero_pratica'):
        return ""

class createDocx(object):

    def __init__(self,context,request):
        self.context = context
        self.request = request

    def __call__(self):
        return ""