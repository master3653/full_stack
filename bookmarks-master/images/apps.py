# -*- coding:utf-8 -*-
__author__ = 'Lin_Tong'

from django.apps import AppConfig
class ImagesConfig(AppConfig):
    name = 'images'
    verbose_name = 'Images bookmarks'
    def ready(self):

        import images.signals