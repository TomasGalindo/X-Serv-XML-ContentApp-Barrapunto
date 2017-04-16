from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
from barrapunto.models import Page
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
# Create your views here.

content_Rss = ""


class myContentHandler(ContentHandler):
    texto = ""

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement(self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement(self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.texto += ("<div><p>Title: " + self.theContent + ".</p>")
                # To avoid Unicode trouble
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.texto += ("<p>Link: " + "<a href=" + self.theContent +
                               ">" + self.theContent + "</a></p></div>")
                self.inContent = False
                self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


def writeBase(request):
    respuesta = "Listado de las paginas que tienes guardadas. "
    lista_paginas = Page.objects.all()
    for pagina in lista_paginas:
        respuesta += "<br>" + pagina.name + " --> Id = " + str(pagina.id)
    respuesta += "<br>Debe buscar por Id"
    return HttpResponse(respuesta)


@csrf_exempt
def pagina(request, identificador):
    if request.method == "GET":
        # Buscar en la base de datos
        try:
            pagina = Page.objects.get(id=identificador)
            # si existe
            respuesta = ("<html><body><div>" + pagina.page + "</div><div>" +
                         content_Rss + "</div></body></html>")
        except Page.DoesNotExist:
            # no existe
            respuesta = "No existe la pagina con el ID = " + str(identificador)

    elif request.method == "PUT":
        cuerpo = request.body.decode('utf-8')
        name, page = cuerpo.split(",")
        pagina = Page(name=name, page=page)
        pagina.save()
        respuesta = "He detectado un PUT, Guardado en Base de datos"
    else:
        respuesta = "Metodo No Permitido"
    return HttpResponse(respuesta)


def update(request):
    # detecto update
    global content_Rss
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    url = "http://barrapunto.com/index.rss"
    f = urllib.request.urlopen(url)
    theParser.parse(f)
    # saco el contetn_Rss
    content_Rss = theHandler.texto
    respuesta = ("<html><body><div>Noticias Barrapunto: " + content_Rss +
                 "</div></body></html>")
    return HttpResponse(respuesta)


def notFound(request, rec):
    respuesta = "Elemento " + rec + " no encontrado"
    return HttpResponse(respuesta)
