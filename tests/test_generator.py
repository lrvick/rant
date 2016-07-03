from unittest import TestCase, main
from mock import MagicMock, mock_open, patch
from rant.generator import Generator
import datetime

SOURCE_DIR = 'tests/test_site'
DEST_DIR = 'tests/test_site/deploy'
TEST_POST = '%s/posts/2016-07-02-2101-test_post.md' % SOURCE_DIR
TEST_POST_PARSED = {
  'permalink': 'test_post',
  'title': 'test post',
  'content': '<p>Test Post</p>',
  'date': datetime.datetime(2016, 7, 2, 21, 1, 16),
  'draft': False,
  'layout': 'post',
  'comments': True,
  'tags': ['hello', 'world']
}
TEST_PAGE = '%s/pages/test_page.md' % SOURCE_DIR
PAGE_FILES = [TEST_PAGE]
POST_FILES = [TEST_POST]
POST_FILENAME = 'tests/test_site/deploy/blog/test_post/index.html'
NAVIGATION = ['blog', 'test page']


class TestGenerate(TestCase):
    def setUp(self):
        self.generator = Generator(SOURCE_DIR, DEST_DIR)

    def test_find_source_files(self):
        self.assertEqual(
            POST_FILES,
            self.generator._find_source_files('post')
        )
        self.assertEqual(
            PAGE_FILES,
            self.generator._find_source_files('page')
        )

    def test_get_navigation(self):
        self.assertEqual(
            NAVIGATION,
            self.generator._get_navigation()
        )

    def test_parse_file(self):
        self.assertEqual(
            TEST_POST_PARSED,
            self.generator._parse_file(TEST_POST)
        )

    def test_render_html(self):
        self.assertEqual(
            open(POST_FILENAME, 'r').read(),
            self.generator._render_html(TEST_POST_PARSED, 'post')
        )

    def test_write_html(self):
        fake_file = mock_open()
        with patch("builtins.open", fake_file, create=True):
            self.generator._write_html('<p>Test</p>', 'test_post', 'post')
        fake_file.assert_called_once_with(POST_FILENAME, 'wb', 1)
        fake_file.return_value.write.assert_called_once_with(b'<p>Test</p>')


if __name__ == '__main__':
    main()
