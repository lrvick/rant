from unittest import TestCase, main
from mock import patch, MagicMock, call
from rant.init import Initializer

DEST_DIR = 'tests/test_site'


class TestInitialize(TestCase):

    def setUp(self):
        self.initializer = Initializer(DEST_DIR)

    def test_create_tree(self):
        with patch("rant.init.os", MagicMock()) as mock_os:
            mock_os.makedirs = MagicMock()
            self.initializer._create_tree()
            mock_os.makedirs.assert_has_calls([
                call('tests/test_site/posts'),
                call('tests/test_site/pages'),
                call('tests/test_site/deploy'),
                call('tests/test_site/deploy/blog')
            ])

    def test_copy_defaults(self):
        with patch("rant.init.shutil", MagicMock()) as mock_shutil:
            mock_shutil.copy = MagicMock()
            mock_shutil.copytree = MagicMock()

            self.initializer._copy_defaults()
            mock_shutil.copy.assert_called_with(
                '%s/defaults/config.yml' % self.initializer._rant_path,
                'tests/test_site'
            )
            mock_shutil.copytree.assert_called_with(
                '%s/defaults/layouts' % self.initializer._rant_path,
                'tests/test_site/layouts'
            )

    def test_init_notempty(self):
        with patch("rant.init.os", MagicMock()) as mock_os:
            mock_os.listdir = MagicMock(return_value=['foo'])
            self.assertEqual(self.initializer.init(), False)

    def test_init(self):
        self.initializer._create_tree = create_tree = MagicMock()
        self.initializer._copy_defaults = copy_defaults = MagicMock()

        with patch("rant.init.os", MagicMock()) as mock_os:
            mock_os.listdir = MagicMock(return_value=[])
            self.initializer.init()

        copy_defaults.assert_called_once()
        create_tree.assert_called_once()

if __name__ == '__main__':
    main()
