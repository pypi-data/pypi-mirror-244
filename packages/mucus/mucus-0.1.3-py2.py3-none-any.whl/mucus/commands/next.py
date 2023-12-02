import mucus.command

import yaspin


class Command(mucus.command.Command):
    def __call__(self, player, **kwargs):
        player.events.stop.set()
        with yaspin.yaspin():
            player.thread.join()
        player.start()
