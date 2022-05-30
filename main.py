import random
import slugify
from pytube import YouTube
from moviepy import editor
from bs4 import BeautifulSoup

with open('YouTube Music.html', 'r', encoding='utf8') as html:
    soup = BeautifulSoup(html.read(), 'lxml')

    container = soup.find('ytmusic-playlist-shelf-renderer')
    tracks = container.find_all('ytmusic-responsive-list-item-renderer')

    for idx, t in enumerate(tracks):
        div = t.find('div', class_='title-column')
        a = div.find('a')
        link = a.attrs['href'].replace('music.', '').split('&')[0]

        print(link)

        try:
            v = YouTube(link)
            s = v.streams.get_highest_resolution()
            path = s.download('video')
        except Exception as e:
            print(e)
            print(f'video {idx} raised an exception')
            continue

        v = editor.VideoFileClip(path)
        audio = v.audio

        title = path.replace('video', 'music').split('\\')[-1].split('.')[0]
        title = slugify.slugify(title) or str(random.random())
        title = f'{idx}_{title}'

        print(title)

        audio.write_audiofile(
            ('\\'.join(path.replace('video', 'music').split('\\')[:-1]) + '\\' + title + '.mp3')
        )
