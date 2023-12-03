"""Client entry point for the command line program.

"""
__author__ = 'Paul Landes'

from typing import Dict, Tuple, Any
import sys
import logging
from pathlib import Path
import plac
from zensols.pybuild import Tag, SetupUtil

logger = logging.getLogger(__name__)


# The version of the applicatin
# *Important*: must also be updated in src/python/setup.py
VERSION = '0.1.1'


class WriteUtil(object):
    def __init__(self, output_format: str = 'text', setup_path: Path = None):
        self.output_format = output_format
        if setup_path is None:
            setup_path = SetupUtil.DEFAULT_SETUP_FILE
            if not setup_path.is_file():
                paths: Tuple[Path, ...] = tuple(Path('.').glob('**/setup.py'))
                if len(paths) == 0:
                    raise OSError('No setup.py found in current directory tree')
        self.setup_path = Path(setup_path)

    def write(self):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'setup path: {self.setup_path}')
        sutil = SetupUtil.source(start_path=self.setup_path)
        if self.output_format == 'json':
            sutil.to_json()
        else:
            sutil.write()


@plac.annotations(
    action=(('the action to take ' +
             '(CREATE tag, DELete tag LAST tag, RECREATE last tag)'),
            'positional', None, str,
            'create del recreate last info write'.split()),
    repodir=('path of the repository', 'option', 'r', Path),
    message=('documentation for the new tag', 'option', 'm', str),
)
def _main(action: str, repodir: Path = '.', message: str = 'none'):

    prog: str = Path(sys.argv[0]).name
    params: Dict[str, Any] = dict(repo_dir=repodir)
    log_level: int = logging.WARNING
    if action not in {'last', 'info', 'write'}:
        log_level = logging.INFO
    if action == 'create':
        params['message'] = message
    logging.basicConfig(level=log_level, format=f'{prog}: %(message)s')
    {
        'create': lambda: Tag(**params).create(),
        'del': lambda: Tag(**params).delete_last_tag(),
        'recreate': lambda: Tag(**params).recreate_last_tag(),
        'last': lambda: print(Tag(**params).last_tag),
        'info': lambda: Tag(**params).to_json(),
        'write': lambda: WriteUtil().write(),
    }[action]()


def main():
    plac.call(_main)
