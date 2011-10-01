from scrapy.spider import BaseSpider, Request
from scrapy.selector import HtmlXPathSelector
from parl import items
import re
import sys

# http://www.parlament.ch/ab/frameset/d/n/4820/361145/d_n_4820_361145_361319.htm
# http://www.parlament.ch/ab/toc/d/n/4820/361145/d_n_4820_361145_361319.htm

class ParlSpider(BaseSpider):
    name = "www.parlament.ch"
    allowed_domains = ["www.parlament.ch"]
    base_url = "http://www.parlament.ch" 
    start_urls = [
        # NR 2011
        "http://www.parlament.ch/ab/toc/d/n/4820/d_n_4820.htm", # Autumn 11
        "http://www.parlament.ch/ab/toc/d/n/4819/d_n_4819.htm", # Summer 11
        "http://www.parlament.ch/ab/toc/d/n/4818/d_n_4818.htm", # April (special) 11
        "http://www.parlament.ch/ab/toc/d/n/4817/d_n_4817.htm", # Spring 11
        # SR 2011
        "http://www.parlament.ch/ab/toc/d/s/4820/d_s_4820.htm", # Autum 11
        "http://www.parlament.ch/ab/toc/d/s/4819/d_s_4819.htm", # Summer 11
        "http://www.parlament.ch/ab/toc/d/s/4817/d_s_4817.htm", # Spring 11

    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sessions = hxs.select('//a[@id="MeetingTitleLink"]/@href').extract()
        for link in sessions:
            yield Request(self.base_url+link, self.parse_subpage)

    def parse_subpage(self, response):
        hxs = HtmlXPathSelector(response)
        subjects = hxs.select("//a[@id='SubjectTitleLink']/@href").extract()
        for link in subjects:
            yield Request(self.base_url+link.replace("/frameset/", "/toc/"), self.parse_detail)
    
    def parse_detail(self, response):
        hxs = HtmlXPathSelector(response)
        #subjects = hxs.select("//a[@id='SubjectTitleLink']/*/span/text()").extract()
        matchSpeakerInfo = re.compile("^([^(]*) \(([^,]*), (.*)\)$")
        subjects = []
        speakers = []
        currentSubject = False
        for tr in hxs.select("//tr"):
            id = tr.select('@id').extract()
            if len(id) > 0:
                if id[0] == "SubjectTitleLine":
                    subjectParts = tr.select(".//span/text()").extract()
                    if currentSubject:
                        subjects.append(currentSubject)
                    currentSubject = items.Subject(id=subjectParts[0], title= " ".join(subjectParts[1:]), speakers=[])
                    
                elif id[0] == "SpeachTitleLine":

                    speakerDesc = tr.select(".//a[@id='SpeachTitleLink']//span/text()").extract()
                    speakerDesc = speakerDesc[0]
                    if speakerDesc:
                        try:
                            name, group, canton = matchSpeakerInfo.match(speakerDesc).groups()
                            speaker = items.Speaker(subjectId=currentSubject['id'], name=name, group=group, canton=canton, detailPage=tr.select(".//a[@id='SpeachTitleLink']/@href").extract()[0])
                            speakers.append(speaker)
                        except AttributeError:
                            print "No matched speaker for", speakerDesc

        if currentSubject:
            subjects.append(currentSubject)
        return speakers
