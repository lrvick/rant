from time import gmtime, strftime
from datetime import datetime
from unittest import TestCase, main
from mock import patch, MagicMock
from rant.create import Creator

TIME = gmtime()
TIMESTAMP = datetime(*TIME[:6]).strftime("%Y-%m-%d-%H%M")
DEST_DIR = 'tests/test_site'
RENDERED_POST = """---
layout: post
title: ''
date: %s
tags: []
comments: true
draft: false
---\n""" % strftime('%Y-%m-%d %H:%M:%S', TIME)
RENDERED_PAGE = """---
layout: page
title: ''
date: %s
---\n""" % strftime('%Y-%m-%d %H:%M:%S', TIME)


class TestCreator(TestCase):

    def setUp(self):
        self.creator = Creator(DEST_DIR)
        self.creator._time = TIME

    def test_render_template(self):
        with patch("rant.create.gmtime", MagicMock()) as mock_gmtime:
            mock_gmtime.return_value = TIME
            self.creator._layout = 'post'
            self.assertEqual(
                self.creator._render_template(),
                RENDERED_POST
            )
            self.creator._layout = 'page'
            self.assertEqual(
                self.creator._render_template(),
                RENDERED_PAGE
            )

    def test_get_savepath_post(self):
        self.creator._layout = 'post'
        self.assertEqual(
            self.creator._get_savepath('some title'),
            'tests/test_site/posts/%s-some_title.md' % TIMESTAMP
        )

    def test_get_savepath_page(self):
        self.creator._layout = 'page'
        self.assertEqual(
            self.creator._get_savepath('some title'),
            'tests/test_site/pages/some_title.md'
        )

    def test_get_temppath(self):
        with patch("rant.create.NamedTemporaryFile", MagicMock) as mock_ntf:
            mock_ntf.name = '/tmp/sometemp'
            mock_ntf.write = MagicMock()
            temppath = self.creator._get_temppath(RENDERED_POST)
            self.assertEqual(temppath, '/tmp/sometemp')
            mock_ntf.write.assert_called_once_with(
                RENDERED_POST.encode("UTF-8")
            )

    def test_launch_editor(self):
        with patch("rant.create.system", MagicMock()) as mock_system:
            with patch("rant.create.environ", MagicMock()) as mock_environ:
                mock_environ.get = MagicMock(return_value="nano")
                self.creator._launch_editor('somefile')
                mock_system.assert_called_once_with('nano somefile')

    def test_create(self):
        with patch("rant.create.Parser", MagicMock) as mock_parser:
            with patch("rant.create.copyfile", MagicMock()) as mock_copyfile:
                self.creator._render_template = render_template = MagicMock()
                self.creator._get_temppath = get_temppath = MagicMock()
                self.creator._launch_editor = launch_editor = MagicMock()
                self.creator._get_savepath = get_savepath = MagicMock()
                mock_parser.parse = parse = MagicMock(
                    return_value={'title': 'sometitle'}
                )
                get_temppath.return_value = 'tempfile'
                get_savepath.return_value = 'savefile'
                render_template.return_value = RENDERED_POST

                self.creator.create()
                render_template.assert_called_once()
                get_temppath.assert_called_once_with(RENDERED_POST)
                launch_editor.assert_called_once_with('tempfile')
                parse.assert_called_once()
                get_savepath.assert_called_once_with('sometitle')
                mock_copyfile.assert_called_once_with('tempfile', 'savefile')

if __name__ == '__main__':
    main()
