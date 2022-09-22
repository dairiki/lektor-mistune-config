# lektor-mistune-config

Beginnings of an attempt at a Lektor plugin to make configuration of the mistune
Markdown processor simple.

I'm also playing with using `hatch` to build the distribution and to run the tests
and manage the development environment.

See lektor/lektor#1076, where the idea was suggested by @nixjdm.

Currently this requires Lektor from the `master` branch of https://github.com/lektor/lektor
**with** PRs lektor/lektor#1074 and lektor/lektor#1073 manually merged in as well.

## Instructions

Currently, this plugin looks for a config file in
`configs/mistune-config.ini` (relative to the Lektor project root.)
Two settings are currently checked: `mistune2.plugins` and
`mistune2.extra-plugins`.  Plugins listed in `plugins` will *replace*
the default set of plugins normally enabled by Lektor.  Plugins set in
`extra-plugins` will augment the default set of plugins (or the
plugins set by `plugins` if they have been so overridden.)

E.g. to add the [abbr](https://mistune.readthedocs.io/en/latest/plugins.html#abbr)
plugin to the set of enabled plugins:


```ini
[mistune2]
extra-plugins = abbr
```

or, to enable only the `abbr` plugin (and disable plugins such as `strikethrough` which Lektor
normally enables by default):

```ini
[mistune2]
plugins = abbr
```


## Running the tests

Currently, it's a bit of a pain to run the tests as you'll need to manually build a Lektor `.whl`
that includes PRs lektor/lektor#1074 and lektor/lektor#1073.

Put the `.whl` somewhere and edit the
`tool.hatch.envs.default.dependencies` array in `pyproject.toml` to
declare that `.whl` as a dependency.

Then
```sh
hatch run cov
```
should run the tests (such as they are.)
