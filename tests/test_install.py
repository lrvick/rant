from unittest import TestCase, main
from mock import patch, MagicMock, call
from rant.install import Installer

DEST_DIR = 'tests/test_site'


class TestInstaller(TestCase):

    def setUp(self):
        self.installer = Installer(DEST_DIR)

    def test_create_tree(self):
        with patch("rant.install.makedirs", MagicMock()) as makedirs:
            self.installer._create_tree()
            makedirs.assert_has_calls([
                call('tests/test_site/posts'),
                call('tests/test_site/pages'),
                call('tests/test_site/static'),
                call('tests/test_site/deploy'),
                call('tests/test_site/deploy/blog')
            ])

    def test_copy_defaults(self):
        with patch("rant.install.copy", MagicMock()) as copy:
            with patch("rant.install.copytree", MagicMock()) as copytree:

                self.installer._copy_defaults()
                copy.assert_called_with(
                    '%s/defaults/config.yml' % self.installer._rant_path,
                    'tests/test_site'
                )
                copytree.assert_has_calls([
                    call('%s/defaults/layouts' % self.installer._rant_path,
                         'tests/test_site/layouts'),
                    call('%s/defaults/css' % self.installer._rant_path,
                         'tests/test_site/static/css')
                ])

    def test_install_notempty(self):
        with patch("rant.install.listdir", MagicMock()) as listdir:
            listdir.return_value = ['foo']
            self.assertEqual(self.installer.install(), False)

    def test_install(self):
        self.installer._create_tree = create_tree = MagicMock()
        self.installer._copy_defaults = copy_defaults = MagicMock()

        with patch("rant.install.listdir", MagicMock()) as listdir:
            listdir.return_value = []
            self.installer.install()

        copy_defaults.assert_called_once()
        create_tree.assert_called_once()

if __name__ == '__main__':
    main()
