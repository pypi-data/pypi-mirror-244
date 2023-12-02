import click

import mucus.command


class Command(mucus.command.Command):
    def __call__(self, player, **kwargs):
        if player.state is None:
            return
        try:
            song = player.state['song']
        except KeyError:
            return
        if song is None:
            return
        click.echo(' '.join([
            click.style(song.artist, fg='green'),
            click.style(song.title, fg='blue')
        ]))
