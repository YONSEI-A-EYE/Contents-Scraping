import scrapy
import html as h
import re 
import pandas as pd
import json 

num=0
file_path_csv = 'C:/Users/shong/Desktop/A_EYE/theme_title_artist.csv'

def remove_tag(content):
    cleanr =re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', content)

    return cleantext

invalid_page_url=False
class Spider1Spider(scrapy.Spider):
    name = "bugs" #$ scrapy crawl bugs

    def start_requests(self): 
        allowed_domains = ['https://music.bugs.co.kr']
        theme_ids=[5729, 5712, 5963, 6161, 6142, 6174, 240, 6889, 10849, 1440, 10504, 14684, 13617, 19752, 4093, 4796]
        theme_names=['사랑/기쁨','이별/슬픔','스트레스/짜증','우울할때','지치고 힘들때','멘붕/불안','그리움','외로울때','썸 탈때',
                    '고백','울고 싶을때','새벽감성','싱숭생숭','설렘/심쿵','기분전환','힐링']

        for i in range(len(theme_ids)):
            for page_id in range(1,6):
                url=f"https://music.bugs.co.kr/musicpd?order=list&tag_id={theme_ids[i]}&order=view&page={page_id}" #rank by popularity
                yield scrapy.Request(url=url, callback=self.get_playlist, meta={'theme':theme_names[i]})
        
    def get_playlist(self, response):
        theme = response.meta['theme']
        for i in range(len(response.css("figcaption.info > a"))):
            url=response.css("figcaption.info > a")[i].get().split('"')[1]
            yield scrapy.Request(url=url, callback=self.get_music,meta={'theme':theme, 'url':url})

    def get_music(self, response):
        theme = response.meta['theme']
        url=response.meta['url']
        for i in range(len(response.css('table.list  > tbody > tr'))):
            playlist_id=url.split('/')[5].split('?')[0]
            title=response.css(f'#ESALBUM{playlist_id} > table > tbody > tr:nth-child({i+1}) > th > p > a').get().split(">")[1].split("<")[0].replace(",", " ")
            artist=response.css(f'#ESALBUM{playlist_id} > table > tbody > tr:nth-child({i+1}) > td:nth-child(7) > p > a').get().split(">")[1].split("<")[0].replace(",", " ")
            lyric_url=response.css(f'#ESALBUM{playlist_id} > table > tbody > tr:nth-child({i+1}) > td:nth-child(5) > a').get().split('"')[1]
            yield scrapy.Request(url=lyric_url, callback=self.get_theme_title_artist, meta={'theme':theme, 'title':title, 'artist':artist})

    def get_theme_title_artist(self, response):
        theme = response.meta['theme']
        title = response.meta['title']
        artist = response.meta['artist']

        with open(file_path_csv, 'a' ,encoding="cp949") as f:
            f.write((str(theme)+","+title+" "+artist+"\n"))