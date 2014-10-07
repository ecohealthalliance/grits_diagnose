#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright 2013 Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

import sys
import os

# Insert the directory of this file to the path so that the plugin
# picks up the mocked grits-api package.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests import base

admin = {
    'email': 'grits@email.com',
    'login': 'grits',
    'firstName': 'grits',
    'lastName': 'grits',
    'password': 'gritspassword',
    'admin': True
}

privUser = {
    'email': 'gritsPriv@email.com',
    'login': 'gritsPriv',
    'firstName': 'First',
    'lastName': 'Last',
    'password': 'goodpassword',
    'admin': False
}

gritsUser = {
    'email': 'gritsUser@email.com',
    'login': 'gritsUser',
    'firstName': 'First',
    'lastName': 'Last',
    'password': 'goodpassword',
    'admin': False
}

normalUser = {
    'email': 'normalUser@email.com',
    'login': 'normalUser',
    'firstName': 'First',
    'lastName': 'Last',
    'password': 'goodpassword',
    'admin': False
}


def setUpModule():
    base.enabledPlugins.append('grits_diagnose')

    base.startServer()


def tearDownModule():
    base.stopServer()


class DiagnoseTestCase(base.TestCase):

    def setUpGroups(self):
        self.admin = self.model('user').createUser(**admin)
        self.normalUser = self.model('user').createUser(**normalUser)
        self.model('group').createGroup(**{
            'name': 'GRITS',
            'creator': self.admin,
            'description': '',
            'public': False
        })
        self.model('group').createGroup(**{
            'name': 'GRITSPriv',
            'creator': self.admin,
            'description': '',
            'public': False
        })

    def testGritsPermissions(self):

        def requests(user, params, status):
            resp = self.request(
                path='/resource/diagnose',
                params=params,
                method='POST',
                user=user
            )
            self.assertStatus(resp, status[0])

        self.setUpGroups()

        # test admin permissions
        requests(self.admin, {}, (200, 200))

        # test non grits user permissions
        requests(self.normalUser, {}, (403, 403))

        # test normal grits user permissions
        gritsGroup = self.model('group').find({'name': 'GRITS'})[0]
        user = self.model('user').createUser(**gritsUser)
        self.model('group').addUser(gritsGroup, user)

        requests(user, {}, (200, 403))

        # test privilaged grits user permissions
        privGroup = self.model('group').find({'name': 'GRITSPriv'})[0]
        user = self.model('user').createUser(**privUser)
        self.model('group').addUser(privGroup, user)
        self.model('group').addUser(gritsGroup, user)

        requests(user, {}, (200, 200))
