# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
import lxml.html

ROOT_URL = 'http://www.deliveryextra.com.br'

# Read in a page
html = scraperwiki.scrape("http://www.deliveryextra.com.br/secoes")

# Find something on the page using css selectors
root = lxml.html.fromstring(html)

try:

    for el in root.cssselect("div.listaDepartamentoWrapper li a"):
        href = el.get('href')
        secao = el.cssselect('span')[0].text

        print href

        scraperwiki.sqlite.save(unique_keys=['secao', 'href'],
                                data={"secao": secao, "href": href},
                                table_name='secoes')

    for secao in scraperwiki.sql.select("* FROM secoes"):
        try:
            html = scraperwiki.scrape(secao['href'])
            root = lxml.html.fromstring(html)

            for el in root.cssselect("div.listaDepartamentoWrapper li a"):
                href = el.get('href')
                subsecao = el.cssselect('span')[0].text

                print href

                scraperwiki.sqlite.save(unique_keys=['subsecao', 'href'],
                                        data={"secao": secao['secao'], "subsecao": subsecao, "href": href},
                                        table_name='subsecoes')
        except ValueError:
            pass

    for subsecao in scraperwiki.sql.select("* FROM subsecoes"):
        try:
            html = scraperwiki.scrape(subsecao['href'])
            root = lxml.html.fromstring(html)

            for el in root.cssselect("table.listagemProdutos tbody tr"):

                imagem = ROOT_URL + el.cssselect("td:nth-child(1) img")[0].get('src')
                href = el.cssselect("td:nth-child(2) a")[0].get('href')
                produto = el.cssselect("td:nth-child(2) a span")[0].text
                preco = el.cssselect("td:nth-child(3).prdValor strong")[0].text

                print href

                scraperwiki.sqlite.save(unique_keys=['produto', 'href'],
                                        data={"secao": subsecao['secao'],
                                              "subsecao": subsecao['subsecao'],
                                              "produto": produto,
                                              "imagem": imagem,
                                              "preco": preco,
                                              "href": href},
                                        table_name='produtos')
        except ValueError:
            pass
except TypeError:
    import pdb; pdb.set_trace()
