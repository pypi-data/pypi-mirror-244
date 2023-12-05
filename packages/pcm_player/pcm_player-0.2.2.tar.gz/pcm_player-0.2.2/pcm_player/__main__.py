import logging
import sys
import argparse

from .pcm_player import PcmPlayer
from . import __version__

def cli():
    try:
        parser = argparse.ArgumentParser("pcm_player", description="Commandline Python application for playing MSU PCM files")
        parser.add_argument("-f", "--file", help="The PCM file to play", type=str)
        parser.add_argument("-l", "--loop", help="Test the loop point by playing just the end of the song and the loop", action='store_true')
        parser.add_argument("-v", "--version", help="Get the version number", action='store_true')
        args = parser.parse_args()

        if args.version == True:
            print("pcm_player v"+__version__)
            return

        if not args.file:
            print("usage: pcm_player [-h] [-f FILE] [-l] [-v]")
            return

        player = PcmPlayer(args.file)

        result = player.validate_file()
        if result == False:
            return

        if args.loop == True:
            player.test_loop()
        else:
            player.play_song()

    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    cli()