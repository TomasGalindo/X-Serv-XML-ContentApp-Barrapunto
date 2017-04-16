#! /usr/bin/python3
import xml_parser_barrapunto
from xml.sax import make_parser
import urllib.request
import webapp


class contentApp (webapp.webApp):
    content = {'/': 'Root page',
               '/page': 'A page'
              }
    
    def parse(self, request):
        metodo = request.split(' ', 1)[0]
        recurso = request.split(' ', 2)[1]
        body = request.split('\r\n\r\n')[1]

        return (metodo, recurso, body)

    def process(self,parsed):
        metodo, resourceName, body = parsed
        if metodo == "GET":
            if resourceName in self.content.keys():
                # MIra en el dicionario y saca el recurso
                # hacer todo lo del parser
                theParser = make_parser()
                theHandler = xml_parser_barrapunto.myContentHandler()
                theParser.setContentHandler(theHandler)
                url = "http://barrapunto.com/index.rss"
                f = urllib.request.urlopen(url)
                theParser.parse(f)
                # saco el contetn_Rss
                content_Rss = theHandler.texto
                httpCode = "200 OK"
                htmlBody = ("<html><body><div>Pagina buscada: " +
                            self.content[resourceName] +
                            "</div><div>Noticias Barrapunto: " + content_Rss +
                            "</div></body></html>")
            else:
                httpCode = "404 Not Found"
                htmlBody = "Element Not Found"
        elif metodo == "PUT":
            # Tengo que guardar las cosas en el diccionario
            self.content[resourceName] = body
            httpCode = "200 OK"
            htmlBody = "PUT Detectado. Guardado en  el diccionario"
        else:
            httpCode = "405 Method Not Allowed"
            htmlBody = "No se puede utilizar ese método"

        return (httpCode, htmlBody)

if __name__ == "__main__":
    testWebApp = contentApp("localhost", 1234)
