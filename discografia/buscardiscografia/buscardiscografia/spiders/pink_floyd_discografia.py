import scrapy

class PinkFloydDiscografiaSpider(scrapy.Spider):
    name = 'pink_floyd_discografia'
    start_urls = ['https://pt.wikipedia.org/wiki/Discografia_de_Pink_Floyd']

    def parse(self, response):
        table = response.xpath('//table[contains(@class, "wikitable")][1]')
        rows = table.xpath('.//tr[td]')
        total_rows = len(rows)
        
        current_year = None
        for idx, row in enumerate(rows):
            # Pular a última linha
            if idx == total_rows - 1:
                continue
            
            year = row.xpath('.//td[1]//text()').get()
            album_details = row.xpath('.//td[2]//a[1]/text()').get()
            
            # Verifica se a linha contém informações válidas e ignora as linhas indesejadas
            if album_details and '—' in album_details:
                continue
            
            # Atualiza current_year se um novo ano for encontrado, caso contrário, usa o ano anterior
            if year:
                current_year = year.strip()
            else:
                year = current_year

            yield {
                'ano': current_year if current_year else None,
                'album': album_details.strip() if album_details else None,
            }
