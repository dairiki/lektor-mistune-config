from lektor.pluginsystem import Plugin


class MistuneConfigPlugin(Plugin):
    """A Lektor plugin to help configure mistune."""

    name = "Mistune Config"
    description = "Easy configuration of mistune Markdown rendering for Lektor"

    def on_markdown_config(self, config, **extra) -> None:
        cfg = self.get_config()
        plugins = cfg.get("mistune2.plugins")
        extra_plugins = cfg.get("mistune2.extra-plugins")
        if plugins is None and extra_plugins is None:
            return
        parser_options = getattr(config, "parser_options", None)
        if parser_options is None:
            # FIXME: warn no plugin support
            return  # running under mistune 0.x — no plugins
        if "plugins" not in parser_options:
            # FIXME: warn no plugin support
            return  # early Lektor 3.4.0b — no plugin resolution support

        if plugins is not None:
            # overwrite default plugin list
            parser_options["plugins"] = plugins.split()
        if extra_plugins is not None:
            parser_options["plugins"].extend(extra_plugins.split())
