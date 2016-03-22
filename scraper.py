# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
import lxml.html

# Read in a page
html = scraperwiki.scrape("http://www.deliveryextra.com.br/secoes")

# Find something on the page using css selectors
root = lxml.html.fromstring(html)


for el in root.cssselect("div.listaDepartamentoWrapper li a"):
    href = el.get('href')
    secao = el.findall('span')[0].text

    scraperwiki.sqlite.save(unique_keys=['secao', 'href'],
                            data={"secao": secao, "href": href},
                            table_name='secoes')

for secao in scraperwiki.sql.select("* FROM secoes"):
    html = scraperwiki.scrape(secao['href'])
    root = lxml.html.fromstring(html)

    for el in root.cssselect("div.listaDepartamentoWrapper li a"):
        href = el.get('href')
        subsecao = el.findall('span')[0].text

        scraperwiki.sqlite.save(unique_keys=['subsecao', 'href'],
                                data={"subsecao": subsecao, "href": href},
                                table_name='subsecoes')
