'''* ------------------------------------------------
   * A simple script to download songs in mp3 format
   * from Youtube.
   * Users pass the song name as arguement.
   * -------------------------------------------------
   * Deepjyoti Barman
   * deepjyoti30@github.com'''

from __future__ import unicode_literals
import youtube_dl
import os
import glob
import sys
import shutil
from colorama import init
from colorama import Fore, Style
import argparse
import setupConfig
from print import PREPEND
from defaults import DEFAULT
import song
import yt

# init colorama for windows
init()

def arguments():
    # Parse the arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('SONG_NAME', help = "Name of the song to download.", type = str)
    parser.add_argument('-q', '--quiet', help = "Don't ask the user to select songs if more than one search result.\
                        The first result in each case will be considered.", action = 'store_true')

    args = parser.parse_args()

    return args



def cleanup():
    # Move the song from temp to $HOME/Music dir
    try:
        SONG = glob.glob(os.path.join(DEFAULT.SONG_TEMP_DIR, '*mp3'))
        SONG = SONG[0]

        SONG_NAME = os.path.basename(SONG)
        shutil.move(SONG, os.path.join(DEFAULT.SONG_DIR, SONG_NAME))

        return True
    except:
        return False

#-----------------------------------------------

def main():

    args = arguments()
    song_name = args.SONG_NAME
    is_quiet = args.quiet

    if is_quiet:
        PREPEND(1)
        print('Quiet is enabled') 

    PREPEND(1)
    print('Searching Youtube for ', end='')
    print(Fore.LIGHTYELLOW_EX, end='')
    print(song_name,end='')
    print(Style.RESET_ALL)

    data, urls = yt.search(song_name)

    if len(data) > 1 and not is_quiet:
        # Ask for a choice
        choice = song.getChoice(data, 'mp3')
    else:
        choice = 0
    
    link = 'https://youtube.com{}'.format(urls[int(choice)])

    PREPEND(1)
    print('Downloading ', end='')
    print(Fore.LIGHTMAGENTA_EX,end='')
    print(data[choice]['title'], end=' ')
    print(Style.RESET_ALL, end='')
    print('to ' + DEFAULT.SONG_TEMP_DIR + ' in',end=' ')
    print(Fore.LIGHTYELLOW_EX,end='')
    print(DEFAULT.SONG_QUALITY + 'kbps',end='')
    print(Style.RESET_ALL)
    if not yt.GRAB_SONG(link):
        PREPEND(2)
        print('Something went wrong while downloading!\a')
        sys.exit(0)
    else:
        PREPEND(1)
        print('Downloaded!')

    PREPEND(1)
    print('Getting song data...')

    TRACK_INFO = song.getData(song_name)

    if TRACK_INFO == False:
        PREPEND(2)
        print('Exiting now!\a')
        cleanup()
        sys.exit(0)
    elif len(TRACK_INFO) == 0:
        PREPEND(2)
        print('No data was found!\a')
        sys.exit(0)
    else:
        PREPEND(1)
        print('Data downloaded!')

    PREPEND(1)
    print('Setting data...')

    if not song.setData(TRACK_INFO, is_quiet):
        PREPEND(2)
        print('Something went wrong while writing data!\a')
        sys.exit(0)

    PREPEND(1)
    print('Moving to Music directory...')

    if not cleanup():
        PREPEND(2)
        print('Something went wrong while moving!\a')
        sys.exit(0)
    else:
        PREPEND(1)
        print('Done!')


main()
