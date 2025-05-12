import os
import sys
import json
import subprocess
import shutil
import pytest

# Add the Franko directory to Python path so tests can import validate.py and franko.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Franko')))

from validate import NameInput
from franko import Franko


def test_nameinput_splitting():
    """
    If parts are provided as a single string, NameInput should split them correctly.
    """
    ni = NameInput(parts="Іван Петрович", gender="masculine")
    assert ni.parts == ["Іван", "Петрович"]
    assert ni.gender == "masculine"


def test_nameinput_invalid_replacement():
    """
    Invalid characters in a name part should be replaced with '-'.
    """
    ni = NameInput(parts=["Іван", "123!", "Петрович"], gender="feminine")
    assert ni.parts == ["Іван", "-", "Петрович"]


def test_nameinput_missing_given_raises():
    """
    If all parts are skipped ('-'), NameInput should raise a ValueError.
    """
    with pytest.raises(ValueError):
        NameInput(parts=["-", "-"], gender="masculine")


def test_franko_generate_success(monkeypatch, tmp_path):
    """
    A successful call to Franko.generate should return the parsed JSON output.
    """
    # Mock Node.js presence
    monkeypatch.setattr(shutil, 'which', lambda _: '/usr/bin/node')
    # Make any os.path.isfile call return True
    monkeypatch.setattr(os.path, 'isfile', lambda p: True)

    # Create a fake decline.bundle.js in the temporary directory
    fake_bundle = tmp_path / 'decline.bundle.js'
    fake_bundle.write_text('')

    # Mock subprocess.run to return a predefined JSON output
    dummy_output = {
        'nominative': 'Test',
        'genitive': 'Testa',
        'dative': 'Testu',
        'accusative': 'Testa',
        'instrumental': 'Testom',
        'locative': 'Testu',
        'vocative': 'Teste'
    }
    completed = subprocess.CompletedProcess(
        args=[], returncode=0,
        stdout=json.dumps(dummy_output).encode('utf-8')
    )
    monkeypatch.setattr(subprocess, 'run', lambda *args, **kwargs: completed)

    # Initialize Franko and override the bundle path
    fr = Franko()
    fr.bundle_path = str(fake_bundle)

    # Call generate and verify the result
    result = fr.generate('Іван Петрович', 'masculine')
    assert result == dummy_output


def test_franko_node_missing(monkeypatch):
    """
    If Node.js is not found during initialization, Franko() should raise a RuntimeError.
    """
    monkeypatch.setattr(shutil, 'which', lambda _: None)
    with pytest.raises(RuntimeError):
        Franko()


def test_franko_subprocess_error(monkeypatch, tmp_path):
    """
    If the subprocess call returns a non-zero exit code, generate() should raise a RuntimeError.
    """
    # Mock Node.js presence and file existence
    monkeypatch.setattr(shutil, 'which', lambda _: '/usr/bin/node')
    monkeypatch.setattr(os.path, 'isfile', lambda p: True)

    # Create a fake bundle file
    fake_bundle = tmp_path / 'decline.bundle.js'
    fake_bundle.write_text('')

    # Simulate subprocess error
    completed = subprocess.CompletedProcess(
        args=[], returncode=1,
        stderr=b'Unexpected error'
    )
    monkeypatch.setattr(subprocess, 'run', lambda *args, **kwargs: completed)

    fr = Franko()
    fr.bundle_path = str(fake_bundle)
    with pytest.raises(RuntimeError) as excinfo:
        fr.generate('Іван', 'masculine')
    assert 'Node.js error' in str(excinfo.value)
