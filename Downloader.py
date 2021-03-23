#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from cfscrape import create_scraper
from requests import session
from tqdm import tqdm


class Downloader(object):
    def __init__(self, download_url, backup_url, output, header, show_info, settings):
        self.sess = session()
        self.sess = create_scraper(self.sess)

        self.show_name = show_info[0]
        self.season = re.search(r'(\d+)', show_info[1]).group(1).zfill(settings.get_setting('seasonPadding'))
        if show_info[2] == "":
            self.episode = '{0}'.format(re.search(r'(\d+)', show_info[3]).group(1).zfill(
                settings.get_setting('episodePadding')))
        else:
            self.episode = '{0}'.format(re.search(r'(\d+)', show_info[2]).group(1).zfill(
                settings.get_setting('episodePadding')))
        self.desc = show_info[3]
        self.header = header
        self.output = output
        self.backup_url = backup_url

        if settings.get_setting('includeShowDesc'):
            self.file_name = settings.get_setting('saveFormat').format(show=self.show_name, season=self.season,
                                                                       episode=self.episode, desc=self.desc)
        else:
            self.file_name = settings.get_setting('saveFormat').format(show=self.show_name, season=self.season,
                                                                       episode=self.episode)
        self.file_path = self.output + os.sep + "{0}.mp4".format(self.file_name)

        print('[wco-dl] - Downloading {0}'.format(self.file_name))
        while True:
            if not self.start_download(download_url):
                print('[wco-dl] - Trying to download using the backup URL...')
                if not self.start_download(self.backup_url):
                    print(f'[wco-dl] - Download for {self.file_name} did not complete, '
                          f'please create an issue on GitHub.\n')
                    f_path = os.path.dirname(os.path.realpath(__file__)) + os.sep
                    f = open(f_path + "failed.txt", "a+")
                    f.write("{0},{1},{2}".format(self.file_name, self.output, show_info[4]))
                    f.close()
                    break
                else:
                    break
            else:
                break

    def start_download(self, url):
        while True:
            dlr = self.sess.get(url, stream=True, headers=self.header)  # Downloading the content using python.
            with open(self.file_path, "wb") as handle:
                for data in tqdm(dlr.iter_content(chunk_size=1024)):  # Added chunk size to speed up the downloads
                    handle.write(data)

            if os.path.getsize(self.file_path) == 0:
                # print("[wco-dl] - Download for {0} did not complete, please try again.\n".format(self.file_name))
                # Upon failure of download append the episode name, file_name, to a text file in the same directory
                # After finishing download all the shows the program will see if that text file exists and attempt
                # to re-download the missing files
                return False
            else:
                print(f'[wco-dl] - Download for {self.file_name} completed.\n')
                return True
