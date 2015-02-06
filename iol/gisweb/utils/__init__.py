from zope.i18nmessageid import MessageFactory
from AccessControl import allow_module
allow_module('iol.gisweb.utils.interfaces')
allow_module('iol.gisweb.utils.IolDocument')
MessageFactory = MessageFactory('iol.gisweb.utils')