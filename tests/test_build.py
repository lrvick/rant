from unittest import TestCase, main
from mock import mock_open, patch, MagicMock, ANY, call
from rant.build import Builder
import datetime

SOURCE_DIR = 'tests/test_site'
DEST_DIR = 'tests/test_site/deploy'
TEST_PAGE = '%s/pages/test_page.md' % SOURCE_DIR
TEST_POST = '%s/posts/2016-07-02-2101-test_post.md' % SOURCE_DIR
TEST_POST_DRAFT = '%s/posts/2016-07-04-1919-test_post_draft.md' % SOURCE_DIR
TEST_CONFIG = {
    'author': 'Your Name',
    'description': 'Your Description Here',
    'disqus_shortname': None,
    'email': 'your@email.com',
    'google_analytics_id': None,
    'paginate': 10,
    'subtitle': 'Your Subtitle Here',
    'title': 'Your Site Name',
    'url': 'http://yoursite.com'
}
TEST_POST_PARSED = {
    'comments': True,
    'content': '<p>Test Post</p>',
    'date': datetime.datetime(2016, 7, 2, 21, 1, 16),
    'draft': False,
    'layout': 'post',
    'permalink': 'blog/test_post',
    'tags': ['hello', 'world'],
    'title': 'test post'
}
TEST_POST_PRERENDER = {
    'current_page': 'blog',
    'navigation': ['blog', 'test page'],
    'config': TEST_CONFIG,
}
PAGE_FILES = [TEST_PAGE]
POST_FILES = [TEST_POST, TEST_POST_DRAFT]
POST_FILENAME = 'tests/test_site/deploy/blog/test_post/index.html'
POST_INDEX_FILENAME = 'tests/test_site/deploy/blog/pages/1/index.html'
NAVIGATION = ['blog', 'test page']
PAGE_POSTS = [
    TEST_POST_PARSED.copy(),
    TEST_POST_PARSED.copy(),
    TEST_POST_PARSED.copy(),
]

class TestGenerate(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.builder = Builder(SOURCE_DIR, DEST_DIR)

    def test_find_source_files(self):
        self.assertEqual(
            POST_FILES,
            self.builder._find_source_files('post')
        )
        self.assertEqual(
            PAGE_FILES,
            self.builder._find_source_files('page')
        )

    def test_get_navigation(self):
        self.assertEqual(
            NAVIGATION,
            self.builder._get_navigation()
        )

    def test_render_html(self):
        fh = open(POST_FILENAME, 'r')
        self.assertEqual(
            fh.read(),
            self.builder._render_html(TEST_POST_PARSED.copy())
        )
        fh.close()

    def test_write_file(self):
        with patch("rant.build.open", mock_open()) as fake_fh:
            with patch("rant.build.os", MagicMock()) as mock_os:

                mock_os.path = MagicMock()
                mock_os.path.isdir = MagicMock(return_value=False)
                mock_os.makedirs = MagicMock()
                self.builder._write_file('<p>Test</p>', 'blog/test_post')

                fake_fh.assert_called_once_with(POST_FILENAME, 'w', 1)
                fake_fh.return_value.write.assert_called_with(
                    '<p>Test</p>'
                )
                mock_os.path.isdir.assert_called_with(
                    'tests/test_site/deploy/blog/test_post'
                )
                mock_os.makedirs.assert_called_with(
                    'tests/test_site/deploy/blog/test_post'
                )

    def test_render_blog_index_page(self):
        fh = open(POST_INDEX_FILENAME, 'r')
        self.assertEqual(
            fh.read(),
            self.builder._render_blog_index_page(
                [TEST_POST_PARSED.copy()],
                1
            )
        )
        fh.close()

    def test_write_blog_index_page_single(self):
        self.builder._per_page = 1
        write_file = MagicMock()
        self.builder._write_file = write_file
        self.builder._write_blog_index_page(PAGE_POSTS, 1)
        write_file.assert_has_calls([
            call(ANY, ''),
            call(ANY, 'blog'),
            call(ANY, 'blog/pages/1')
        ])

    def test_gen_blog_index_page_multiple(self):
        self.builder._per_page = 2
        self.builder._write_file = write_file = MagicMock()
        self.builder._write_blog_index_page(PAGE_POSTS, 2)
        write_file.assert_called_once_with(ANY, 'blog/pages/2')

    def test_gen_contexts(self):
        post = TEST_POST_PARSED.copy()
        post['rendered_html'] = self.builder._render_html(post)
        self.assertEqual(
            self.builder._gen_contexts([TEST_POST]),
            [post]
        )

    def test_gen_contexts_draft(self):
        self.builder.Parser = MagicMock(return_value=None)
        self.assertEqual(
            self.builder._gen_contexts([TEST_POST_DRAFT]),
            []
        )

    def test_write_contexts(self):
        self.builder._write_file = write_file = MagicMock()
        post = TEST_POST_PARSED.copy()
        post['rendered_html'] = self.builder._render_html(post)
        self.builder._write_contexts([post, post, post])
        self.assertEqual(write_file.call_count, 3)

    def test_write_blog_index(self):
        post = TEST_POST_PARSED.copy()
        post['rendered_html'] = self.builder._render_html(post)
        self.builder._per_page = 2
        self.builder._write_blog_index_page = \
            write_blog_index_page = MagicMock()
        self.builder._write_blog_index([post, post, post])
        self.assertEqual(write_blog_index_page.call_count, 2)

    def test_write_feed(self):
        post = TEST_POST_PARSED.copy()
        self.builder._write_file = write_file = MagicMock()
        self.builder._write_feed('rss', [post, post, post])
        write_file.assert_called_once_with(ANY, 'blog', 'rss.xml')

    def test_write_sitemap(self):
        post = TEST_POST_PARSED.copy()
        page = TEST_POST_PARSED.copy()
        self.builder._write_file = write_file = MagicMock()
        self.builder._write_sitemap([post, post, post], [page, page, page])
        write_file.assert_called_once_with(ANY, '', 'sitemap.xml')

    def test_copy_static(self):
        with patch("rant.build.copy_tree", MagicMock()) as copy_tree:
            self.builder._copy_static()
            copy_tree.assert_called_once_with(
                '%s/static' % SOURCE_DIR,
                DEST_DIR
            )

    def test_build(self):
        self.builder._write_contexts = write_contexts = MagicMock()
        self.builder._gen_contexts = gen_contexts = MagicMock()
        self.builder._write_contexts = write_contexts = MagicMock()
        self.builder._write_blog_index = write_blog_index = MagicMock()
        self.builder._write_feed = write_feed = MagicMock()
        self.builder._write_sitemap = write_sitemap = MagicMock()
        self.builder._copy_static = copy_static = MagicMock()

        self.builder.build()
        self.assertEqual(gen_contexts.call_count, 2)
        self.assertEqual(write_contexts.call_count, 2)
        write_blog_index.assert_called_once()
        write_sitemap.assert_called_once()
        copy_static.assert_called_once()
        write_feed.assert_has_calls([
            call('atom', ANY),
            call('rss', ANY),
        ])

if __name__ == '__main__':
    main()
