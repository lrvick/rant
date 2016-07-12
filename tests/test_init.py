import rant
from rant.__init__ import create_parser, process_args
from mock import MagicMock, patch
from unittest import TestCase


class TestCLIParser(TestCase):

    def setUp(self):
        self.parser = create_parser()

    def test_install(self):
        with patch("rant.__init__.Installer", MagicMock) as installer:
            installer.install = MagicMock()
            args = self.parser.parse_args(['install'])
            process_args(args)
            installer.install.assert_called_once()

    def test_create(self):
        with patch("rant.__init__.Creator", MagicMock) as creator:
            creator.create = MagicMock()
            args = self.parser.parse_args(['create'])
            process_args(args)
            creator.create.assert_called_once()

    def test_build(self):
        with patch("rant.__init__.Builder", MagicMock) as builder:
            builder.build = MagicMock()
            args = self.parser.parse_args(['build'])
            process_args(args)
            builder.build.assert_called_once()

    def test_serve(self):
        with patch("rant.__init__.Server", MagicMock) as server:
            server.serve = MagicMock()
            args = self.parser.parse_args(['serve'])
            process_args(args)
            server.serve.assert_called_once()

    def test_main(self):
        with patch("rant.__init__.create_parser", MagicMock()) \
                as create_parser:
            with patch("rant.__init__.process_args", MagicMock()) \
                    as process_args:
                rant.__init__.main()
                create_parser.assert_called_once()
                process_args.assert_called_once()
