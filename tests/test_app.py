import logging
import logging.config
import subprocess
import os
import tempfile
from pathlib import Path


# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

here = Path(__file__).parent

inputPath = Path('tests/in')
log.debug('input path folder: {0}'.format(inputPath.absolute()))

env = os.environ.copy()
env['PYTHONPATH'] = str(here.parent)

def test_help():
    result = subprocess.run(['python3', './qface/app.py', "--help"], stdout=subprocess.PIPE, env=env)
    assert result.returncode == 0
    assert """
Usage: app.py [OPTIONS] [SOURCE]...

Options:
  --rules PATH                [required]
  --target DIRECTORY
  --reload / --no-reload      Auto reload script on changes
  --scaffold / --no-scaffold  Add extrac scaffolding code
  --watch DIRECTORY
  --feature TEXT
  --run TEXT                  run script after generation
  --force / --no-force        forces overwriting of files
  --help                      Show this message and exit.
""", result.stdout

def test_generate():
    tmpDir = tempfile.TemporaryDirectory()
    result = subprocess.run(['python3', './qface/app.py', "--rules", "tests/app_templates/rules.yaml", "--target", tmpDir.name, "--force", "tests/in/com.pelagicore.ivi.tuner.qface"], stdout=subprocess.PIPE, env=env)
    assert result.returncode == 0
    assert """
merge: com.pelagicore.ivi.tuner.yaml
process: frontend
""", result.stdout

def test_generate_and_run():
    tmpDir = tempfile.TemporaryDirectory()
    result = subprocess.run(['python3', './qface/app.py', "--rules", "tests/app_templates/rules.yaml", "--target", tmpDir.name, "--force", "tests/in/com.pelagicore.ivi.tuner.qface", "--run", "echo DONE"], stdout=subprocess.PIPE, env=env)
    assert result.returncode == 0
    assert """
merge: com.pelagicore.ivi.tuner.yaml
process: frontend
$ echo DONE
DONE
""", result.stdout

