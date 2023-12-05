"""Light tests to verify that the wheel works

Just import things
"""

import os
import platform
import sys

import pytest


@pytest.mark.parametrize("feature", ["curve", "ipc"])
def test_has(feature):
    import zmq

    if (
        feature == 'ipc'
        and sys.platform == 'win32'
        and platform.python_implementation() == "CPython"
    ):
        # Windows wheels lack IPC
        # pending release with https://github.com/zeromq/libzmq/pull/4422
        assert not zmq.has(feature)
    else:
        assert zmq.has(feature)


def test_simple_socket():
    import zmq

    ctx = zmq.Context()
    s = ctx.socket(zmq.PUSH)
    s.close()
    ctx.term()


@pytest.mark.skipif(
    sys.platform != "win32" or platform.python_implementation() != "CPython",
    reason="only on CPython + Windows",
)
def test_bundle_msvcp():
    import zmq

    zmq_dir = os.path.abspath(os.path.dirname(zmq.__file__))
    # pyzmq.libs is *next to* zmq itself
    pyzmq_lib_dir = os.path.join(zmq_dir, os.pardir, "pyzmq.libs")
    dlls = []
    if os.path.exists(pyzmq_lib_dir):
        dlls = sorted(
            name for name in os.listdir(pyzmq_lib_dir) if name.endswith(".dll")
        )
    print(dlls)
    # Is concrt140 needed? delvewheel doesn't detect it anymore
    should_bundle = ["msvcp140.dll"]
    vcruntime = "vcruntime140.dll"
    shouldnt_bundle = []
    if platform.python_implementation() == 'PyPy':
        should_bundle = []
    elif sys.version_info < (3, 10):
        shouldnt_bundle.append(vcruntime)

    for dll in shouldnt_bundle:
        assert dll not in dlls

    for dll in should_bundle:
        assert dll in dlls

    assert any(dll.startswith("libzmq") for dll in dlls)
    assert any(dll.startswith("libsodium") for dll in dlls)
