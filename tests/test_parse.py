from unittest import TestCase, main
from rant.parse import Parser
from datetime import datetime

SOURCE_DIR = 'tests/test_site'
DEST_DIR = 'tests/test_site/deploy'
TEST_PAGE = '%s/pages/test_page.md' % SOURCE_DIR
TEST_POST = '%s/posts/2016-07-02-2101-test_post.md' % SOURCE_DIR
TEST_POST_DRAFT = '%s/posts/2016-07-04-1919-test_post_draft.md' % SOURCE_DIR
TEST_POST_PARSED = {
    'comments': True,
    'content': '<p>Test Post</p>',
    'date': datetime(2016, 7, 2, 21, 1, 16),
    'draft': False,
    'layout': 'post',
    'permalink': 'blog/test_post',
    'tags': ['hello', 'world'],
    'title': 'test post'
}
TEST_PAGE_PARSED = {
    'content': '<p>test page</p>',
    'date': datetime(2016, 7, 2, 21, 1, 16),
    'layout': 'page',
    'permalink': 'test_page',
    'title': 'test page'
}


class TestParser(TestCase):
    def setUp(self):
        self.post_parser = Parser(TEST_POST)
        self.draft_parser = Parser(TEST_POST_DRAFT)
        self.page_parser = Parser(TEST_PAGE)

    def test_parse_post(self):
        self.assertEqual(
            self.post_parser.parse(),
            TEST_POST_PARSED
        )

    def test_parse_page(self):
        self.assertEqual(
            self.page_parser.parse(),
            TEST_PAGE_PARSED
        )

    def test_parse_post_draft(self):
        self.assertEqual(
            self.draft_parser.parse(),
            None
        )


if __name__ == '__main__':
    main()
