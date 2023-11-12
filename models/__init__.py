#!/usr/bin/python3

""" This module contains initializaation of the file storage """

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
