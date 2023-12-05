from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from unittest import TestCase

from freezegun import freeze_time

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest, HttpResponse
from django.test import Client

from .storage import TitofistoStorage
from .views import TitofistoUploadView

test_file_1 = b"The quick brown fox jumps over the lazy dog"
test_file_1_name = "quickfox.dat"


class TitofistoMediaTestCase(TestCase):
    def setUp(self):
        self.storage = TitofistoStorage()

        self.test_file_1 = b"The quick brown fox jumps over the lazy dog"
        self.test_file_1_name = "quickfox.dat"
        self.storage.save(self.test_file_1_name, BytesIO(self.test_file_1))

        self.test_file_2 = b"Franz jagt im komplett verwahrlosten Taxi quer durch Bayern"
        self.test_file_2_name = "franztaxi.dat"
        self.storage.save(self.test_file_2_name, BytesIO(self.test_file_2))

        self.test_file_3 = b"Franz jagt im komplett verwahrlosten Taxi quer durch Bayern"
        self.test_file_3_name = "public/franztaxi.dat"
        self.storage.save(self.test_file_3_name, BytesIO(self.test_file_3))

        self.param = "titofisto_token"
        self.timeout = 60 * 60
        self.client = Client()

    def tearDown(self):
        self.storage.delete(self.test_file_1_name)
        self.storage.delete(self.test_file_2_name)

    def test_token_deterministic(self):
        """The generated token is deterministic for a single, unchanged file"""
        with freeze_time():
            token_1 = self.storage.get_token(self.test_file_1_name)
            token_2 = self.storage.get_token(self.test_file_1_name)

        self.assertEqual(token_1, token_2)

    def test_token_file_dependent(self):
        """The generated token is different for different files"""
        with freeze_time():
            token_1 = self.storage.get_token(self.test_file_1_name)
            token_2 = self.storage.get_token(self.test_file_2_name)

        self.assertNotEqual(token_1, token_2)

    def test_token_ts_dependent(self):
        """The generated token is different for different timestamps"""
        with freeze_time():
            token_1 = self.storage.get_token(self.test_file_1_name)
        with freeze_time():
            token_2 = self.storage.get_token(self.test_file_2_name)

        self.assertNotEqual(token_1, token_2)

    def test_get_valid_token(self):
        """A file can be retrieved with a valid token"""
        token = self.storage.get_token(self.test_file_1_name)

        url = f"{settings.MEDIA_URL}{self.test_file_1_name}?" f"{self.param}={token}"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.streaming_content)[0], self.test_file_1)

    def test_get_invalid_token(self):
        """A file can not be retrieved with an invalid token"""
        token = self.storage.get_token(self.test_file_1_name)

        url = f"{settings.MEDIA_URL}{self.test_file_1_name}?" f"{self.param}=a{token}"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 404)

    def test_get_close_to_timeout(self):
        """A file can still be retrieved close to the timeout"""
        now = datetime.now()
        with freeze_time(now + timedelta(seconds=self.timeout - 1)):
            token = self.storage.get_token(self.test_file_1_name)
            url = f"{settings.MEDIA_URL}{self.test_file_1_name}?" f"{self.param}={token}"
            res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.streaming_content)[0], self.test_file_1)

    def test_get_after_timeout(self):
        """A file can not be retrieved after the timeout"""
        now = datetime.now()
        with freeze_time(now):
            token = self.storage.get_token(self.test_file_1_name)
            url = f"{settings.MEDIA_URL}{self.test_file_1_name}?" f"{self.param}={token}"
        with freeze_time(now + timedelta(seconds=self.timeout + 1)):
            res = self.client.get(url)

        self.assertEqual(res.status_code, 404)

    def test_get_after_mtime_change(self):
        """A file can not be retrieved with the same token after its mtime changes"""
        now = datetime.now()
        with freeze_time(now + timedelta(seconds=10)):
            token = self.storage.get_token(self.test_file_1_name)
            url = f"{settings.MEDIA_URL}{self.test_file_1_name}?" f"{self.param}={token}"
            Path(self.storage.path(self.test_file_1_name)).touch()
        res = self.client.get(url)

        self.assertEqual(res.status_code, 404)

    def test_url(self):
        """The URL for a file should contain a token."""
        url1 = self.storage.url(self.test_file_1_name)
        url2 = self.storage.url(self.test_file_2_name)
        self.assertIn(self.param, url1)
        self.assertIn(self.param, url2)

    def test_public_files_url(self):
        """The URL for a file in the public namespace doesn't contain a token."""
        url = self.storage.url(self.test_file_3_name)
        self.assertNotIn(self.param, url)

    def test_public_files_view(self):
        """A file in the public namespace can be acessed without a token."""
        self.storage.url(self.test_file_3_name)
        url = f"{settings.MEDIA_URL}{self.test_file_3_name}"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_404_not_found(self):
        """A 404 is returned for non-existent files."""
        url = f"{settings.MEDIA_URL}public/some_not_existing_file.txt"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)


def _upload_cb_test_1(request) -> HttpResponse:
    file = request.FILES["file"]
    assert file.name == test_file_1_name
    assert file.read() == test_file_1

    return HttpResponse(status=418)


def _upload_cb_test_2(request, p1, p2, foo) -> HttpResponse:
    assert p1 == "pos1"
    assert p2 == "pos2"
    assert foo == "bar"

    file = request.FILES["file"]
    assert file.name == test_file_1_name
    assert file.read() == test_file_1

    return HttpResponse(status=420)


class TitofistoUploadTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_upload_valid_slot_no_args(self):
        upload_url = TitofistoUploadView.get_upload_slot("titofisto.tests._upload_cb_test_1")
        res = self.client.post(
            upload_url, data={"file": SimpleUploadedFile(test_file_1_name, test_file_1)}
        )

        assert res.status_code == 418

    def test_upload_valid_slot_with_args(self):
        upload_url = TitofistoUploadView.get_upload_slot(
            "titofisto.tests._upload_cb_test_2", ("pos1", "pos2"), {"foo": "bar"}
        )
        res = self.client.post(
            upload_url, data={"file": SimpleUploadedFile(test_file_1_name, test_file_1)}
        )

        assert res.status_code == 420

    def test_upload_invalid_slot(self):
        upload_url = TitofistoUploadView.get_upload_slot("titofisto.tests._upload_cb_test_1")
        upload_url_mangled = upload_url[:-1] + "a/"
        res = self.client.post(
            upload_url_mangled, data={"file": SimpleUploadedFile(test_file_1_name, test_file_1)}
        )

        assert res.status_code == 404

    def test_upload_valid_slot_twice(self):
        upload_url = TitofistoUploadView.get_upload_slot("titofisto.tests._upload_cb_test_1")
        res1 = self.client.post(
            upload_url, data={"file": SimpleUploadedFile(test_file_1_name, test_file_1)}
        )
        res2 = self.client.post(
            upload_url, data={"file": SimpleUploadedFile(test_file_1_name, test_file_1)}
        )

        assert res1.status_code == 418
        assert res2.status_code == 404
