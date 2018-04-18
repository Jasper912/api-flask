#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import actapp
import time

if __name__ == "__main__":
    # Do not use ``run()`` in a production setting. It is not intended to
    # meet security and performance requirements for a production server.
    # Instead, see :ref:`deployment` for WSGI server recommendations.
    print "server run at %s" % (time.strftime("%Y-%m-%d %H:%M:%S"))
    actapp.run(host='0.0.0.0', port=2800, debug=True)
