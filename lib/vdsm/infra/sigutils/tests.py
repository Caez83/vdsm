#
# Copyright 2014 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#

import contextlib
import errno
import os
import signal
import subprocess
import time

from nose import tools

CHILD_SCRIPT = 'tests_child.py'


def assert_read(stream, expected):
    while True:
        try:
            tools.assert_equals(stream.read(len(expected)), expected)
        except IOError as e:
            if e.errno != errno.EINTR:
                raise
        else:
            break


@contextlib.contextmanager
def child_test(*args):
    proc = subprocess.Popen(
        [os.path.abspath(CHILD_SCRIPT)] + list(args),
        stdout=subprocess.PIPE,
        cwd=os.path.dirname(__file__)
    )
    try:
        yield proc
    finally:
        proc.wait()


def test_signal_received():
    with child_test('check_signal_received') as child:
        assert_read(child.stdout, 'ready\n')
        child.send_signal(signal.SIGUSR1)
        assert_read(child.stdout, 'signal sigusr1\n')
        assert_read(child.stdout, 'done\n')


def test_signal_timeout():
    TIMEOUT = 0.2
    with child_test('check_signal_timeout', str(TIMEOUT)) as child:
        now = time.time()
        assert_read(child.stdout, 'ready\n')
        assert_read(child.stdout, 'done\n')
        later = time.time()

        # 3 is a safety factor
        tools.assert_true(TIMEOUT < (later - now) < TIMEOUT * 3)


def test_signal_3_times():
    '''
    A sanity test to make sure wait_for_signal fires more than once.
    '''
    with child_test('check_signal_times') as child:
        assert_read(child.stdout, 'ready\n')
        child.send_signal(signal.SIGUSR1)
        assert_read(child.stdout, 'signal sigusr1\n')
        assert_read(child.stdout, 'woke up\n')
        child.send_signal(signal.SIGUSR1)
        assert_read(child.stdout, 'signal sigusr1\n')
        assert_read(child.stdout, 'woke up\n')
        child.send_signal(signal.SIGUSR1)
        assert_read(child.stdout, 'signal sigusr1\n')
        assert_read(child.stdout, 'woke up\n')
        assert_read(child.stdout, 'done\n')


def test_signal_to_thread():
    with child_test('check_child_signal_to_thread') as child:
        assert_read(child.stdout, 'ready\n')
        assert_read(child.stdout, 'signal sigchld\n')
        assert_read(child.stdout, 'done\n')


def test_uninitialized():
    with child_test('check_uninitialized') as child:
        assert_read(child.stdout, 'ready\n')
        assert_read(child.stdout, 'exception\n')
        assert_read(child.stdout, 'done\n')


def test_register_twice():
    with child_test('check_register_twice') as child:
        assert_read(child.stdout, 'ready\n')
        assert_read(child.stdout, 'exception\n')
        assert_read(child.stdout, 'done\n')
