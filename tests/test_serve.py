from unittest import TestCase, main
from mock import MagicMock, patch
from rant.serve import Server

SOURCE_DIR = 'tests/test_site'
DEST_DIR = 'tests/test_site/deploy'


class TestGenerate(TestCase):
    def setUp(self):
        self.server = Server(SOURCE_DIR, DEST_DIR)

    def test_build(self):
        with patch("rant.serve.Builder", MagicMock()):

            self.server._server = MagicMock()
            self.server._server.watch = MagicMock()
            self.server._server.serve = MagicMock()

            self.server.serve()
            self.server._server.watch.assert_called_once()
            self.server._server.serve.assert_called_once()

if __name__ == '__main__':
    main()
