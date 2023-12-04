from dataclasses import dataclass
import importlib
import logging
import os
from packaging.requirements import Requirement
from pathlib import Path
import sys
from typing import Dict, Any, Optional

from envzy import AutoExplorer, ModulePathsList, PackagesDict

from datasphere.config import PythonEnv as PythonEnvConfig
import yaml

logger = logging.getLogger(__name__)


@dataclass
class PythonEnv:
    version: str
    local_modules_paths: ModulePathsList
    pypi_packages: PackagesDict
    pip_options: Optional[PythonEnvConfig.PipOptions] = None

    @property
    def conda_yaml(self) -> str:
        dependencies = [f'python=={self.version}', 'pip']

        libraries = [f'{name}{version}' for name, version in self.pypi_packages.items()]
        if libraries:
            if self.pip_options:
                if self.pip_options.extra_index_urls:
                    libraries = [f'--extra-index-url {url}' for url in self.pip_options.extra_index_urls] + libraries
                if self.pip_options.no_deps:
                    libraries = ['--no-deps'] + libraries
            dependencies.append({'pip': libraries})

        return yaml.dump({'name': 'default', 'dependencies': dependencies}, sort_keys=False)


def define_py_env(main_script_path: str, py_env_cfg: PythonEnvConfig) -> PythonEnv:
    version = None
    local_modules_paths = None
    pypi_packages = None

    if not py_env_cfg.is_fully_manual:
        # User may not add cwd to PYTHONPATH, in case of running execution through `datasphere`, not `python -m`.
        # Since path to python script can be only relative, this should always work.
        sys.path.append(os.getcwd())
        namespace = _get_module_namespace(main_script_path)
        extra_index_urls = []
        if py_env_cfg.pip_options and py_env_cfg.pip_options.extra_index_urls:
            extra_index_urls = py_env_cfg.pip_options.extra_index_urls
        explorer = AutoExplorer(extra_index_urls=extra_index_urls)

        version = '.'.join(str(x) for x in explorer.target_python)
        local_modules_paths = explorer.get_local_module_paths(namespace)
        pypi_packages = {
            name: f'=={version}' for name, version in
            explorer.get_pypi_packages(namespace).items()
        }

        logger.debug('auto-defined python env:\n\tversion: %s\n\tpypi packages: %s\n\tlocal modules: %s',
                     version, local_modules_paths, pypi_packages)

    return PythonEnv(
        version=py_env_cfg.version if py_env_cfg.version else version,
        pypi_packages=_parse_requirements(py_env_cfg.requirements) if py_env_cfg.requirements else pypi_packages,
        local_modules_paths=py_env_cfg.local_modules_paths if py_env_cfg.local_modules_paths else local_modules_paths,
        pip_options=py_env_cfg.pip_options,
    )


def _get_module_namespace(path: str) -> Dict[str, Any]:
    module_spec = importlib.util.spec_from_file_location('module', path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return vars(module)


# TODO: support flags and options such as `--no-deps`, `--extra-index-url`
def _parse_requirements(f: Path) -> PackagesDict:
    lines = [line.strip() for line in f.read_text().strip().split('\n')]
    result = {}
    for line in lines:
        req = Requirement(line)
        assert req.marker is None, f'requirement markers are not supported ({line})'
        assert req.url is None, f'requirement url is not supported ({line})'
        extras = f'[{",".join(sorted(req.extras))}]' if req.extras else ''
        result[req.name + extras] = str(req.specifier)
    return result
