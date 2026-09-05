"""Environment records preserve reproducibility without exposing credentials."""
import hashlib
import json
import os
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from review_provenance import environment_record


def check_environment_is_portable_and_secret_free() -> None:
    distribution = SimpleNamespace(
        metadata={"Name": "example-package", "Home-page": "https://user:secret@example.org"},
        version="1.2.3",
    )
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        lock = b"example-package==1.2.3\n"
        (root / "requirements.txt").write_bytes(lock)
        with patch("review_provenance.REPO", root), patch(
            "review_provenance.distributions", return_value=[distribution]
        ), patch.dict(os.environ, {"INSILICO_LOCKED_ENVIRONMENT": "true", "API_KEY": "secret"}):
            record = environment_record()
        assert record["packages"] == {"example-package": "1.2.3"}
        assert record["lock_sha256"] == hashlib.sha256(lock).hexdigest()
        assert record["lock_applied"] is True
        assert "secret" not in json.dumps(record)
        assert str(root) not in json.dumps(record)
        with patch("review_provenance.REPO", root), patch.dict(os.environ, {}, clear=True):
            assert environment_record()["lock_applied"] is False
