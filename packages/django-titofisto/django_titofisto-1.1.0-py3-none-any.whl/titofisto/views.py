from typing import Any, Optional

from django.core.cache import cache
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.http import FileResponse, Http404, HttpRequest, HttpResponse
from django.urls import reverse
from django.utils.module_loading import import_string
from django.views import View

import shortuuid

from .settings import PARAM, USE_PUBLIC_NAMESPACE, PUBLIC_NAMESPACE, TIMEOUT
from .storage import TitofistoStorage


class TitofistoMediaView(View):
    def get(self, request: HttpRequest, name: str) -> FileResponse:
        # Get storage
        storage = TitofistoStorage()

        if USE_PUBLIC_NAMESPACE:
            # Public files are directly served without needing a token
            if name.startswith(PUBLIC_NAMESPACE):
                if storage.exists(name):
                    return FileResponse(storage._open(name))
                else:
                    raise Http404()

        # Inspect URL parameter
        token = request.GET.get(PARAM, None)
        if token is None:
            raise Http404()

        # Verify token for filename
        try:
            storage.verify_token(name, token)
        except FileNotFoundError:
            raise Http404()
        except (BadSignature, SignatureExpired):
            raise Http404()

        # Finally, serve file from disk if all checks passed
        return FileResponse(storage._open(name))


class TitofistoUploadView(View):
    """Handles time-constrained upload slots for files.

    This view can be used to dynamically handle file uploads that are
    protected with a generic upload slot. The mechanism works by some
    code requesting an upload slot URL, to which a client can then POST
    a file. On successful upload, a callback function is called, where
    the requesting code receives the actual file to handle.

    .. code-block:: python

        from titofisto.views import TitofistoUploadView

        def handle_file(request, pk):
            instance = MyModel.objects.get(pk=pk)
            instance.photo = request.FILES["photo"]
            instance.save()

        # This gets an uplaod URL to pass on to the client
        # On upload, the handler above will be called, with 15 as positional argument
        upload_url = TitofistoUploadView.get_upload_slot(
            "mymodule.handle_file",
            (15,)
        )
    """

    @classmethod
    def get_upload_slot(
        cls,
        cb: str,
        args: Optional[tuple[Any]] = None,
        kwargs: Optional[dict[str, Any]] = None,
    ) -> str:
        """Gets an upload slot URL to pass on to a client.

        :param cb: dotted path to a callable accepting an HttpRequest as first argument,
                   and returning an HttpResponse (or None for 200)
        :param args: a tuple of positional arguments to pass to the callback
        :param kwargs: a dictionary of keyword arguments to pass to the callback
        """
        slot_name = shortuuid.uuid()
        token = ":".join(TimestampSigner().sign(slot_name).split(":")[-2:])

        slot_info = {
            "cb": cb,
            "args": args or tuple(),
            "kwargs": kwargs or {},
        }
        cache.set(f"titofisto.slot:{slot_name}", slot_info, TIMEOUT)

        return reverse("titofisto:upload", kwargs={"slot_name": slot_name, "token": token})

    def post(self, request: HttpRequest, slot_name: str, token: str) -> HttpResponse:
        try:
            TimestampSigner().unsign(":".join((slot_name, token)), max_age=TIMEOUT)
        except (BadSignature, SignatureExpired):
            raise Http404()

        slot_info = cache.get(f"titofisto.slot:{slot_name}")
        if slot_info is None:
            raise Http404()
        cache.delete(f"titofisto.slot:{slot_name}")

        cb = import_string(slot_info["cb"])
        res = cb(request, *(slot_info["args"]), **(slot_info["kwargs"]))
        return res or HttpResponse()
