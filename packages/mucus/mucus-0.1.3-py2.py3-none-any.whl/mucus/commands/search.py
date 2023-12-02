import random

import click

import yaspin

import mucus.command
import mucus.deezer.page
import mucus.history


class Command(mucus.command.Command):
    def __call__(self, client, command, player, **kwargs):
        params = {'query': command['line'], 'nb': 40, 'start': 0}

        def search():
            with yaspin.yaspin():
                page = mucus.deezer.page.Search(client=client, **params)
            for k in page.data['ORDER']:
                results = page.data[k]
                if results:
                    try:
                        results = results['data']
                    except (KeyError, TypeError):
                        pass
                    for result in results:
                        t = result.get('__TYPE__')
                        if t == 'song':
                            yield result
                        elif t == 'artist':
                            artist = mucus.deezer.page.Artist(
                                client=client,
                                art_id=result['ART_ID']
                            )
                            for song in artist:
                                yield song
                        elif t == 'playlist':
                            playlist = mucus.deezer.page.Playlist(
                                client=client,
                                playlist_id=result['PLAYLIST_ID']
                            )
                            for song in playlist:
                                yield song

        def unique(songs):
            seen = set()
            for song in songs:
                if song['SNG_ID'] not in seen:
                    yield song
                    seen.add(song['SNG_ID'])

        songs = unique(search())

        while True:
            choices = []
            while len(choices) < 10:
                try:
                    choices.append(next(songs))
                except StopIteration:
                    break
            if len(choices) == 0:
                break
            for i, track in enumerate(choices):
                click.echo(' '.join([
                    click.style(f'{i:02}', fg='red'),
                    click.style(track['ART_NAME'], fg='green'),
                    click.style(track['SNG_TITLE'], fg='blue')
                ]))
            with mucus.history.History(__name__):
                try:
                    i = input('# ')
                except EOFError:
                    return
            shuffle = False
            if i == '.':
                continue
            elif ':' in i:
                if '*' in i:
                    shuffle = True
                    i = i.replace('*', '')
                i = slice(*map(lambda x: x.isdigit() and int(x) or None, i.split(':'))) # noqa
            else:
                try:
                    i = int(i)
                except ValueError:
                    return
                i = slice(i, i+1)
            songs = choices[i]
            if shuffle:
                random.shuffle(songs)
            for choice in songs:
                player.queue.put(choice)
            break
