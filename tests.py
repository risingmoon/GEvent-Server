import unittest
from server import (
    check_uri, map_uri,
    parse_request, build_response,
    Error404, Error405)


class GEventServerTest(unittest.TestCase):

    def test_check_uri_exist(self):
        uri = [
            "/",
            "/images",
            "/images/JPEG_example.jpg",
            "/images/Sample_Scene_Balls.jpg",
            "/images/sample_1.png",
            "a_web_page.html",
            "make_time.py",
            "sample.txt"]
        for num in xrange(6):
            self.assertTrue(check_uri(uri[num]))

    def test_check_uri_not_exist(self):
        uri = [
            "/foobar",
            "/images/foosball.jpg"]
        for num in xrange(2):
            with self.assertRaises(Error404):
                check_uri(uri[num])

    def test_map_uri_images(self):
        uri = [
            "/images/JPEG_example.jpg",
            "/images/Sample_Scene_Balls.jpg",
            "/images/sample_1.png"]

        expected = [
            "image/jpeg",
            "image/jpeg",
            "image/png"]

        for num in xrange(3):
            self.assertEqual(map_uri(uri[num])[1], expected[num])

    def test_directory_uri(self):
        uri = [
            "/",
            "/images"]

        expected = [
            "text/plain",
            "text/plain"]
        for num in xrange(2):
            self.assertEqual(map_uri(uri[num])[1], expected[num])

    def test_file_uri(self):
        uri = [
            "a_web_page.html",
            "make_time.py",
            "sample.txt"]

        expected = [
            "text/html",
            "text/x-python",
            "text/plain"]
        for num in xrange(3):
            self.assertEqual(map_uri(uri[num])[1], expected[num])

    def test_request_forbidden(self):
        message = """POST /hi.html HTTP/1.1\r\n
        \Host: www.example.com \r\n
        \<CRLF>"""
        with self.assertRaises(Error405):
            parse_request(message)

    def test_request_permitted(self):
        message = """GET /sample.txt HTTP/1.1\r\n
        \Host: www.example.com \r\n
        \<CRLF>"""
        body, content_type = parse_request(message)
        response = build_response(body, content_type)
        expected_text = """This is a very simple text file.
Just to show that we can server it up.
It is three lines long."""
        self.assertIn(expected_text, response)
        
if __name__ == "__main__":
    unittest.main()
