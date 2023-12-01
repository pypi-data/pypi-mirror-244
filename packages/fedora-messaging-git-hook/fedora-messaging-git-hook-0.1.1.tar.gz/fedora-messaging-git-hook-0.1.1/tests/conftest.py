# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import pytest


# This is only necessary for pytest < 3.9.0, as in EPEL8
# We can drop this when we no longer need to support it.
@pytest.fixture
def tmp_path(tmpdir):
    return Path(tmpdir)
