# -*- coding: utf-8 -*-
'''
Created on 2014年10月12日

@author: kent
'''
from django.conf import settings

from django.core.files.uploadhandler import MemoryFileUploadHandler

class faceDetectHandler(MemoryFileUploadHandler):
    def file_complete(self, file_size):
        pass

    def receive_data_chunk(self, raw_data, start):
        pass