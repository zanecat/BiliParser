import subprocess
from os import listdir
from os.path import isfile, join
import os
import threading
import time

class Uploader():
    upload_list = []
    def set_upload_list(self, list):
        self.upload_list = list

    def get_file_list(self, dir_path):
        files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
        return files

    def get_name_by_file(self, file_name: str, prefix: str=''):
        if file_name.endswith('.flv'):
            return file_name.replace('.flv', '') + prefix
        else:
            return file_name + prefix

    def print_upload_list(self):
        print('\n')
        print('unfinished: ')
        print(self.upload_list)
        print('\n')
        print('count: '+ str(len(self.upload_list)))
        print('\n')

    def upload_dir(self, dir_path: str, list_to_use=[], file_prefix: str='', category: str = ''):
        self.upload_list = list_to_use if list_to_use else self.get_file_list(dir_path)

        while len(self.upload_list) > 0:
            for file in self.upload_list:
                self.upload_file(dir_path, file, file_prefix, category)
                # thread = threading.Thread(target=self.upload_file, args=(dir_path, file, file_prefix, category,))
                # thread.start()
                time.sleep(60)
            self.print_upload_list()


    def print_line(self, text):
        print('\n')
        print(text)
        print('\n')

    def upload_file(self, dir_path, file_name, file_prefix='', category=''):
        full_path = dir_path + '/' + file_name
        self.print_line('uploading start: ' + full_path)
        try:
            category_str = 'category=' + category if category else ''
            cmd = 'youtube-upload --title=' + file_prefix + self.get_name_by_file(file_name) \
                  + ' ' + full_path + ' ' + category_str
            # output = os.popen().read()
            output = subprocess.check_output(cmd, shell=True)
            if 'error' or 'exception' in output:
                raise Exception(output)
            else:
                self.print_line('uploading finish: ' + full_path)
                self.upload_list.remove(file_name)
        except Exception:
            self.print_line('failed to upload: ' + file_name)