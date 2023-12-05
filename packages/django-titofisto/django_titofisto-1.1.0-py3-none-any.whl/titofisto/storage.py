from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.core.signing import TimestampSigner

from .settings import PARAM, TIMEOUT, USE_PUBLIC_NAMESPACE, PUBLIC_NAMESPACE


class TitofistoStorage(FileSystemStorage):
    """Time-token secured variant of the base filesystem storage."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._signer = TimestampSigner()

    def url(self, name: str) -> str:
        """Compute URL for requested storage file."""
        # Get regular URL from base FileSystemStorage
        raw_url = super().url(name)

        if USE_PUBLIC_NAMESPACE:
            # Public files are accessible without a token
            if name.startswith(PUBLIC_NAMESPACE):
                return raw_url

        # Get token and timestamp
        token = self.get_token(name)

        # Generate full, token-secured URL
        full_url = f"{raw_url}?{PARAM}={token}"
        return full_url

    def get_token_message(self, name: str) -> str:
        """Determine parts of the MAC from the file."""
        if self.exists(name):
            mtime = self.get_modified_time(name).isoformat()
        else:
            mtime = datetime.now().isoformat()
        return f"{name}//{mtime}"

    def get_token(self, name: str) -> str:
        """Get a token for a filename."""
        return ":".join(self._signer.sign(self.get_token_message(name)).split(":")[-2:])

    def verify_token(self, name: str, token: str):
        """Verify a token for validity and timeout."""
        return self._signer.unsign(":".join((self.get_token_message(name), token)), max_age=TIMEOUT)
