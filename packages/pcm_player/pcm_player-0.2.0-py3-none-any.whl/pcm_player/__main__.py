import logging
import sys
import argparse

from .pcm_player import PcmPlayer

def cli():
    try:
        parser = argparse.ArgumentParser("pcm_player", description="Commandline Python application for playing MSU PCM files")
        parser.add_argument("-f", "--file", help="The PCM file to play", type=str, required=True)
        parser.add_argument("-l", "--loop", help="Test the loop point by playing just the end of the song and the loop", action='store_true')
        args = parser.parse_args()

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