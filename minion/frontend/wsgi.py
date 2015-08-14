# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from werkzeug.contrib.fixers import ProxyFix
from minion.frontend import app, configure_app

# Configure the app. Even in production we run with debug as that will
# give us stacktraces in the log. The debug REPL is always disabled.

# It will run in production mode unless MINION_FRONTEND_PRODUCTION is set to no.
production = not bool(
    os.environ.get('MINION_FRONTEND_PRODUCTION', 'yes') == 'no')
app = configure_app(app, production=production, debug=True)
app = ProxyFix(app)
