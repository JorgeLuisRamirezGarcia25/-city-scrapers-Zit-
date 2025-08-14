import scrapy
from city_scrapers_core.spiders import CityScrapersSpider


class ZitacuaroMeetingsSpider(CityScrapersSpider):
    name = "zitacuaro_meetings"
    agency = "Ayuntamiento de Zitácuaro y SEHAZ"
    timezone = "America/Mexico_City"
    start_urls = [
        "https://www.zitacuaro.gob.mx/",
        "https://www.sehaz.org/mx/",
        "https://consultapublicamx.plataformadetransparencia.org.mx/vut-web/faces/view/consultaPublica.xhtml?idEntidad=MTY=&idOrgano=MTY=&idSujetoObligado=MzUyNw==#inicio",
        "https://suemzit.site123.me/"
    ]

    def parse(self, response):
        # Scraping para zitacuaro.gob.mx
        if "zitacuaro.gob.mx" in response.url:
            # Buscar enlaces de prensa en toda la página, no solo en la principal
            links = set(response.xpath('//a[contains(@href, "/prensa_")]/@href').getall())
            # También buscar enlaces de prensa en los scripts y otros atributos
            links.update(response.xpath('//*[contains(@onclick, "/prensa_")]/@onclick').re(r"'(/prensa_\d+)'"))
            for link in links:
                url = response.urljoin(link)
                yield scrapy.Request(url, callback=self.parse_noticia)
        # Scraping para suemzit.site123.me
        elif "suemzit.site123.me" in response.url:
            # Buscar bloques de noticias, eventos o publicaciones
            items = response.xpath('//div[contains(@class, "s123-module-content") or contains(@class, "s123-module-text") or contains(@class, "s123-module-news") or contains(@class, "s123-module-blog")]')
            for item in items:
                title = item.xpath('.//h1/text() | .//h2/text() | .//h3/text()').get()
                date = item.xpath('.//time/text()').get()
                description = " ".join(item.xpath('.//text()').getall()).strip()
                if title and description:
                    yield {
                        "title": title,
                        "date": date,
                        "description": description,
                        "source": response.url,
                    }
        # Scraping para sehaz.org/mx
        elif "sehaz.org/mx" in response.url:
            eventos = response.xpath('//div[contains(@class, "event") or contains(@class, "evento") or contains(@class, "agenda")]')
            for evento in eventos:
                yield {
                    "title": evento.xpath('.//h2/text() | .//h3/text()').get(),
                    "start": evento.xpath('.//time/@datetime').get(),
                    "description": evento.xpath('.//p/text()').get(),
                    "location": evento.xpath('.//span[contains(@class, "lugar")]/text()').get(),
                    "source": response.url,
                }
        # Scraping para Plataforma Nacional de Transparencia
        elif "plataformadetransparencia.org.mx" in response.url:
            tablas = response.xpath('//table')
            for tabla in tablas:
                filas = tabla.xpath('.//tr')
                for fila in filas:
                    columnas = fila.xpath('.//td')
                    if len(columnas) >= 2:
                        yield {
                            "title": columnas[0].xpath('string(.)').get(),
                            "description": columnas[1].xpath('string(.)').get(),
                            "source": response.url,
                        }

    def parse_noticia(self, response):
        title = response.xpath('//h3/text() | //h2/text()').get()
        date = response.xpath('//*[contains(text(),"Marzo") or contains(text(),"Enero") or contains(text(),"Febrero") or contains(text(),"Abril") or contains(text(),"Mayo") or contains(text(),"Junio") or contains(text(),"Julio") or contains(text(),"Agosto") or contains(text(),"Septiembre") or contains(text(),"Octubre") or contains(text(),"Noviembre") or contains(text(),"Diciembre")]/text()').get()
        description = " ".join(response.xpath('//div//text()').getall()).strip()
        yield {
            "title": title,
            "date": date,
            "description": description,
            "source": response.url,
        }
