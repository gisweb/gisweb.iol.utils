from zope.interface import Interface, Attribute


class IIolDocument(Interface):
    """
    marker interface for iol document
    """
    iol_app = Attribute("Application Name")


class IIolLayer(Interface):
    """Marker interface for the Browserlayer
    """
