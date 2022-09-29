import random
import slugify
from multiprocessing import Pool
from datetime import datetime
from pytube import YouTube
from pytube.cipher import get_throttling_function_name
from moviepy import editor
from bs4 import BeautifulSoup


def parse_track(data):
    idx, link = data

    try:
        v = YouTube(link)
        s = v.streams.get_highest_resolution()
        path = s.download('video')
    except Exception as e:
        print(e)
        print(f'video {idx} raised an exception')
        return

    v = editor.VideoFileClip(path)
    audio = v.audio

    title = path.replace('video', 'music').split('\\')[-1].split('.')[0]
    title = slugify.slugify(title) or str(random.random())
    title = f'{idx}_{title}'

    print(title)

    audio.write_audiofile(
        ('\\'.join(path.replace('video', 'music').split('\\')[:-1]) + '\\' + title + '.mp3')
    )


if __name__ == '__main__':
    start_time = datetime.now()

    with open('YouTube Music.html', 'r', encoding='utf8') as html:
        soup = BeautifulSoup(html.read(), 'lxml')

        container = soup.find('ytmusic-playlist-shelf-renderer')
        tracks = container.find_all('ytmusic-responsive-list-item-renderer')
        links = []

        for t in tracks:
            div = t.find('div', class_='title-column')
            a = div.find('a')
            links.append(a.attrs['href'].replace('music.', '').split('&')[0])

        with Pool(10) as pool:
            pool.map(parse_track, enumerate(links))

    print(f'FINISHED BY {start_time - datetime.now()} SEC')
