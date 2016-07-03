from unittest import TestCase, main
from mock import MagicMock
from rant.generator import Generator
import datetime

SOURCE_DIR = 'tests/test_site'
DEST_DIR = '.tmp/test_site'
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
SOURCE_FILES = [TEST_POST, TEST_PAGE]


class TestGenerate(TestCase):
    def setUp(self):
        self.generator = Generator(SOURCE_DIR, DEST_DIR)

    def test_find_source_files(self):
        self.assertEqual(SOURCE_FILES, self.generator._find_source_files())

    def test_parse_file(self):
        self.assertEqual(
            TEST_POST_PARSED,
            self.generator._parse_file(TEST_POST)
        )

if __name__ == '__main__':
    main()
