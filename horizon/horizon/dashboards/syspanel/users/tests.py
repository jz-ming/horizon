# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2011 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.core.urlresolvers import reverse
from mox import IgnoreArg
from openstackx.api import exceptions as api_exceptions

from horizon import api
from horizon import test


USERS_INDEX_URL = reverse('horizon:syspanel:users:index')


class UsersViewTests(test.BaseAdminViewTests):
    def setUp(self):
        super(UsersViewTests, self).setUp()

        self.user = self.mox.CreateMock(api.User)
        self.user.enabled = True
        self.user.id = self.TEST_USER
        self.user.roles = self.TEST_ROLES
        self.user.tenantId = self.TEST_TENANT

        self.users = [self.user]

    def test_index(self):
        self.mox.StubOutWithMock(api, 'user_list')
        api.user_list(IgnoreArg()).AndReturn(self.users)

        self.mox.ReplayAll()

        res = self.client.get(USERS_INDEX_URL)

        self.assertTemplateUsed(res, 'syspanel/users/index.html')
        self.assertItemsEqual(res.context['users'], self.users)

    def test_enable_user(self):
        OTHER_USER = 'otherUser'
        formData = {'method': 'UserEnableDisableForm',
                    'id': OTHER_USER,
                    'enabled': 'enable'}

        self.mox.StubOutWithMock(api, 'user_update_enabled')
        api.user_update_enabled(IgnoreArg(), OTHER_USER, True).AndReturn(
                self.mox.CreateMock(api.User))

        self.mox.ReplayAll()

        res = self.client.post(USERS_INDEX_URL, formData)

        self.assertRedirectsNoFollow(res, USERS_INDEX_URL)

    def test_disable_user(self):
        OTHER_USER = 'otherUser'
        formData = {'method': 'UserEnableDisableForm',
                    'id': OTHER_USER,
                    'enabled': 'disable'}

        self.mox.StubOutWithMock(api, 'user_update_enabled')
        api.user_update_enabled(IgnoreArg(), OTHER_USER, False).AndReturn(
                self.mox.CreateMock(api.User))

        self.mox.ReplayAll()

        res = self.client.post(USERS_INDEX_URL, formData)

        self.assertRedirectsNoFollow(res, USERS_INDEX_URL)

    def test_enable_disable_user_exception(self):
        OTHER_USER = 'otherUser'
        formData = {'method': 'UserEnableDisableForm',
                    'id': OTHER_USER,
                    'enabled': 'enable'}

        self.mox.StubOutWithMock(api, 'user_update_enabled')
        api_exception = api_exceptions.ApiException('apiException',
                message='apiException')
        api.user_update_enabled(IgnoreArg(),
                OTHER_USER, True).AndRaise(api_exception)

        self.mox.ReplayAll()

        res = self.client.post(USERS_INDEX_URL, formData)

        self.assertRedirectsNoFollow(res, USERS_INDEX_URL)
