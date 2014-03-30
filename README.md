GEvent Server
============

This project uses Python code written from http-server repository. The Python code has been refactored to handle concurrencies with GEvent. A "webroot" directory is included. Only GET requests are allowed, and others are forbidden.
Here are request scenarios:

* "127.0.0.1:8000/" - yields directory of webroot folder.
* "127.0.0.1:8000/a_web_page.html" - yields a simple html page.
* "127.0.0.1:8000/make_time.py" - yields an x-Python file.
* "127.0.0.1:8000/sample.txt" - yields a plain text file.
* "127.0.0.1:8000/images" - yields directory of images folder.
* "127.0.0.1:8000/images/JPEG_example.jpeg" - yields directory of images folder.
* "127.0.0.1:8000/images/sample_1.png" - yields directory of images folder.
* "127.0.0.1:8000/images/Sample_Scene_Balls.jpg" - yields directory of images folder.

Code Attribution: [Matt Dougherty](https://github.com/geekofalltrades/)
