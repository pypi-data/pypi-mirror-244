import click

import mucus.command


class Command(mucus.command.Command):
    def __call__(self, player, **kwargs):
        if player.events.loop.is_set():
            player.events.loop.clear()
        else:
            player.events.loop.set()
        click.echo(player.events.loop.is_set() and 'loop' or 'noop')
