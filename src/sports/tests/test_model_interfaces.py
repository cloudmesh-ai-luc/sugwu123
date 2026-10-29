import contextlib
import io
import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from sports.__main__ import main
from sports.demo import demo_rows
from sports.server import make_server
from sports.store import Store


class ModelInterfaceTests(unittest.TestCase):
    def test_cli_and_http_model_results_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.sqlite3"
            store = Store(path)
            store.replace(demo_rows(), kind="synthetic", source="generated", rights="fixture")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main(["--db", str(path), "model", "--team", "Lake City Lynx", "--threshold", "100.5"]), 0)
            server = make_server(store, "127.0.0.1", 0)
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            try:
                query = urlencode({"team": "Lake City Lynx", "threshold": "100.5"})
                with urlopen(f"http://127.0.0.1:{server.server_port}/api/model?{query}") as response:
                    self.assertEqual(json.load(response), json.loads(out.getvalue()))
            finally:
                server.shutdown()
                server.server_close()
                worker.join()
