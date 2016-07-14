from AccessControl import Unauthorized
from DateTime.DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.protectinactive.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.protectinactive.tests.dx_folder import setup_dx_folder
import transaction


class TestTraversalHook(FunctionalTestCase):

    def setUp(self):
        super(TestTraversalHook, self).setUp()
        self.portal = self.layer['portal']
        self.grant('Manager')

        setup_dx_folder(self.portal)

        # no dates
        self.no_dates_atfolder = create(Builder('folder'))
        self.no_dates_dxfolder = create(Builder('dx folder'))

        # active
        effective = DateTime() - 10
        expires = DateTime() + 10
        self.active_atfolder = create(Builder('folder')
                                      .having(effectiveDate=effective,
                                              expirationDate=expires))
        self.active_dxfolder = create(Builder('dx folder')
                                      .having(effectiveDate=effective,
                                              expirationDate=expires))

        # past content
        effective = DateTime() - 20
        expires = DateTime() - 10
        self.past_atfolder = create(Builder('folder')
                                    .having(effectiveDate=effective,
                                            expirationDate=expires))
        self.past_dxfolder = create(Builder('dx folder')
                                    .having(effectiveDate=effective,
                                            expirationDate=expires))

        # future content
        effective = DateTime() + 10
        expires = DateTime() + 20
        self.future_atfolder = create(Builder('folder')
                                      .having(effectiveDate=effective,
                                              expirationDate=expires))
        self.future_dxfolder = create(Builder('dx folder')
                                      .having(effectiveDate=effective,
                                              expirationDate=expires))

    @browsing
    def test_manager_can_access_everything(self, browser):
        browser.login()
        try:
            browser.open(self.no_dates_atfolder)
            browser.open(self.no_dates_dxfolder)
            browser.open(self.active_atfolder)
            browser.open(self.active_dxfolder)
            browser.open(self.past_atfolder)
            browser.open(self.past_dxfolder)
            browser.open(self.future_atfolder)
            browser.open(self.future_dxfolder)
        except Unauthorized:
            self.fail("A Manager has to be able to access all content.")

    @browsing
    def test_editor_can_access_everything(self, browser):
        editor = create(Builder('user').with_roles('Editor', on=self.portal))
        browser.login(editor.getId())

        try:
            browser.open(self.no_dates_atfolder)
            browser.open(self.no_dates_dxfolder)
            browser.open(self.active_atfolder)
            browser.open(self.active_dxfolder)
            browser.open(self.past_atfolder)
            browser.open(self.past_dxfolder)
            browser.open(self.future_atfolder)
            browser.open(self.future_dxfolder)
        except Unauthorized:
            self.fail("An Editor has to be able to access the content.")

    @browsing
    def test_normal_user_access_rights(self, browser):
        user = create(Builder('user'))
        browser.login(user.getId())

        try:
            browser.open(self.no_dates_atfolder)
            browser.open(self.no_dates_dxfolder)
            browser.open(self.active_atfolder)
            browser.open(self.active_dxfolder)
        except Unauthorized:
            self.fail("A normal user has to be able to access active content.")

        with self.assertRaises(Unauthorized):
            browser.open(self.past_atfolder)
        with self.assertRaises(Unauthorized):
            browser.open(self.past_dxfolder)
        with self.assertRaises(Unauthorized):
            browser.open(self.future_atfolder)
        with self.assertRaises(Unauthorized):
            browser.open(self.future_dxfolder)

    @browsing
    def test_user_with_inactive_rights_can_access_past_content(self, browser):
        user = create(Builder('user'))
        browser.login(user.getId())
        self.portal.manage_permission('Access inactive portal content', user.getRoles())
        transaction.commit()

        try:
            browser.open(self.past_atfolder)
            browser.open(self.past_dxfolder)
        except Unauthorized:
            self.fail("User has inactive rights but can't access inactive content.")

        with self.assertRaises(Unauthorized):
            browser.open(self.future_atfolder)
        with self.assertRaises(Unauthorized):
            browser.open(self.future_dxfolder)

    @browsing
    def test_user_with_future_rights_can_access_future_content(self, browser):
        user = create(Builder('user'))
        browser.login(user.getId())
        self.portal.manage_permission('Access future portal content', user.getRoles())

        try:
            browser.open(self.future_atfolder)
            browser.open(self.future_dxfolder)
        except Unauthorized:
            self.fail("User has future rights but can't access future content.")

        with self.assertRaises(Unauthorized):
            browser.open(self.past_atfolder)
        with self.assertRaises(Unauthorized):
            browser.open(self.past_dxfolder)
