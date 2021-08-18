import time

from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest


User = get_user_model()


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session.session_key,
                secure=False,
                path='/'
            )
        )
        self.browser.refresh()


    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edit@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

    def test_logged_in_users_lists_are_saved_ad_my_lists(self):
        
        self.create_pre_authenticated_session('edit@example.com')
        self.browser.get(self.live_server_url)
        self._input_new_item_in_table('Reticulate splines')
        self._input_new_item_in_table('Immanentize eschaton')
        firts_list_url = self.browser.current_url
        self.browser.find_element_by_link_text('My lists').click()

        self.wait_link_text_element('Reticulate splines')
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.assertEqual(self.browser.current_url, firts_list_url)

        self.browser.get(self.live_server_url)
        self._input_new_item_in_table('Click cows')
        second_current_url = self.browser.current_url
        self.browser.find_element_by_link_text('My lists').click()

        self.wait_link_text_element('Click cows')
        self.browser.find_element_by_link_text('Click cows').click()
        self.assertEqual(self.browser.current_url, second_current_url)

        self.browser.find_element_by_link_text('Log out').click()

        self.assertEqual(self.wait_link_text_element('My lists'), [])

