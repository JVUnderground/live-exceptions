import re
import sqlite3
import sys
import traceback

from django.utils.deprecation import MiddlewareMixin

exc_re = re.compile(r'\s*File\s+\"(?P<file>.*)\",\s+line\s+(?P<line_no>\d+),\s+in\s+(?P<parent>\w+)'+'\n(?P<code>.*)\n')

class LiveExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        tb = traceback.format_exception(*(sys.exc_info()))

        # SQLite objects created in a thread can only be used in that same thread
        conn = sqlite3.connect('exceptions.db')
        cur = conn.cursor()

        # Exceptions table
        # UID | TYPE | NAME | USER | SCHEME | HOST | PATH | METHOD
        data = (type(exception).__name__, str(exception), request.user.id, request.scheme, request.META['HTTP_HOST'], request.path, request.method)
        cur.execute('INSERT INTO exceptions VALUES(NULL,?,?,?,?,?,?,?)', data)
        exception_id = cur.lastrowid

        # Traceback table
        # EXCEPTION_ID | FILE | PARENT | LINE_NO | CODE
        for line in tb:
            m = exc_re.match(line)
            if m:
                data = (exception_id, m.group('file'), m.group('parent'), m.group('line_no'), m.group('code'))
                cur.execute('INSERT INTO tracebacks VALUES(?,?,?,?,?)', data)

        conn.commit()
