from typing import Optional

from arraylake.chunkstore.abc import Chunkstore
from arraylake.chunkstore.s3chunkstore import MAX_INLINE_THRESHOLD_BYTES, S3Chunkstore


def chunkstore(chunkstore_uri: str, inline_threshold_bytes: int = 0, **kwargs) -> Chunkstore:
    """Initialize a Chunkstore

    Args:
        chunkstore_uri: URI to chunkstore.
        inline_threshold_bytes: Byte size below which a chunk will be stored in the metastore database. Maximum is 512.
            Values less than or equal to 0 disable inline storage.
        kwargs: Additional keyword arguments to pass to the chunkstore constructor.
    Returns:
        chunkstore:
    """
    if chunkstore_uri and chunkstore_uri.startswith("s3://"):
        return S3Chunkstore(chunkstore_uri, inline_threshold_bytes=inline_threshold_bytes, **kwargs)
    else:
        if chunkstore_uri is None:
            raise ValueError(f"Chunkstore uri is None. Please set your using: `arraylake config set chunkstore.uri URI`.")
        else:
            raise ValueError(f"Cannot parse chunkstore uri {chunkstore_uri}, supported prefixes are: ['s3://']")
