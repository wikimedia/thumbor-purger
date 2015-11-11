# -*- coding: utf-8 -*-

# Copyright (c) 2015, thumbor-community, Wikimedia Foundation
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.

import urllib

from tornado import gen

from thumbor.handlers.imaging import ImagingHandler


class UrlPurgerHandler(ImagingHandler):
    @classmethod
    def regex(cls):
        '''
        :return: The regex used for routing.
        :rtype: string
        '''
        return r'/purge/?(?P<image>.+)?'

    @gen.coroutine
    def get(self, **kw):
        imageurl = urllib.quote(kw['image'].encode('utf8'))

        exists = yield gen.maybe_future(
            self.context.modules.storage.exists(imageurl)
        )

        if exists:
            self.context.modules.storage.remove(imageurl)
            self.set_status(204)
        else:
            self._error(404, 'Image not found at the given URL')

    @gen.coroutine
    def execute_image_operations(self):
        pass
