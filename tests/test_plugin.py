import re

from lektor.context import Context
from lektor.markdown import Markdown
from lektor.project import Project
import pytest


@pytest.fixture
def project(mistune_config, tmp_path):
    project_file = tmp_path / "Test.lektorproject"
    project_file.touch()

    root_contents = tmp_path / "content/contents.lr"
    root_contents.parent.mkdir()
    root_contents.touch()

    if mistune_config:
        cfg_ini = tmp_path / "configs/mistune-config.ini"
        cfg_ini.parent.mkdir()
        with cfg_ini.open("w") as fp:
            for section in mistune_config:
                fp.write(f"[{section}]\n")
                for key, val in mistune_config[section].items():
                    fp.write(f"{key} = {val}\n")

    return Project.from_file(project_file)


@pytest.fixture
def env(project):
    return project.make_env()


@pytest.fixture
def pad(env):
    return env.new_pad()


@pytest.fixture
def render_markdown(pad):
    record = pad.root
    field_options = {}

    def render_markdown(source):
        with Context(pad=pad):
            return str(Markdown(source, record, field_options))

    return render_markdown


@pytest.mark.parametrize("mistune_config, markdown, expect", [
    # `strikethrough` enabled by default
    (None, "~~foo~~", "<del>foo</del>"),
    # Disable all plugins
    ({"mistune2": {"plugins": ""}},
     "~~foo~~", "~~foo~~"),
    # Add additional
    ({"mistune2": {"extra-plugins": "abbr"}},
     "Test HAL ~~9000~~\n\n*[HAL]: Hardware Abstraction Layer",
     r'<abbr title="Hardware .*<del>'),
])
def test_clear_plugins(markdown, expect, render_markdown):
    assert re.search(expect, render_markdown(markdown))
