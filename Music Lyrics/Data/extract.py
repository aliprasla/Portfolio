import requests
from bs4 import BeautifulSoup
import re
def create_album_link_dict(fileName):
    file = open(fileName,'r')
    current_artist = None
    current_links = []
    album_dict = {}
    for line in file:
        if line == '\n':
            continue
        line = line.replace('\n','')
        if current_artist is None:
            current_artist = line
        elif line[0] == '\t':
            line = line.split('\t')
            if (len(line)<3):
                continue
            year = int(line[2])
            line = line[1].replace('\t','')
            album_title = line
            link = 'https://genius.com/albums/{0}/{1}'.format(current_artist.replace(' ','-'),album_title.replace(' ','-').lower())
            current_links.append((album_title,link,year))
        else:
            print(current_artist)
            current_links = list(filter(lambda x:  x != '\n',current_links))
            album_dict[current_artist] = current_links
            current_artist = line
            current_links = []
        current_links = list(filter(lambda x:  x != '\n',current_links))
        album_dict[current_artist] = current_links
            
    return album_dict

def get_album_songs(album_link):
    html = requests.get(album_link).text
    soup = BeautifulSoup(html,"html5lib")
    contents = soup.findAll('div',class_= "chart_row-content")
    song_link = {div.findAll('h3')[0].text.replace('\n','').replace('\t','').strip().replace('\xa0',' ').replace('Lyrics','').rstrip()
                 :div.findAll('a')[0]['href'] for div in contents}
    return song_link
def get_lyrics(link):
    html = requests.get(link).text
    soup = BeautifulSoup(html,'html5lib')
    song_body = soup.findAll('div', class_ = "lyrics")[0]
    lyrics = [line.text for line in song_body.findAll('a')]
    lyrics = [re.sub('\[.*\]','',line).lstrip().replace('\ ','') for line in lyrics]
    lyrics = '\n'.join(lyrics)
    return lyrics

def main():
    import pandas as pd
    link_dict = create_album_link_dict('ExtractSource.txt')
    all_rows = []
    for artist in link_dict.keys():
        for album_name,album_link,year in link_dict[artist]:
            song_link = get_album_songs(album_link)
            for song_name in song_link.keys():
                current_row = {}
                current_row['AlbumName'] = album_name
                current_row['AlbumLink'] = album_link
                current_row['Artist'] = artist
                current_row['SongName'] = song_name
                current_row['SongLink'] = song_link[song_name]
                current_row['Lyrics'] = get_lyrics(song_link[song_name])
                current_row['Year'] = year
                all_rows.append(current_row)
                print(song_name + " - " + artist + " Complete")
        print(album_name + " - " + artist +  " Complete")
    data = pd.DataFrame(all_rows)
    data.to_csv('data.csv',index = False)
    import clean
main()
