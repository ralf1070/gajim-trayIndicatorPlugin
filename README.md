# Gajim Tray Indicator

Gajim plugin that shows the number of unread messages as a badge on the macOS
Dock icon. The badge is also visible in the app switcher (Cmd+Tab).

Gajim has no tray icon support on macOS, so the settings "System tray icon"
and "System tray icon notification" have no effect there.

## Requirements

- macOS (the plugin is only loaded on macOS)
- Gajim 2.6.0 or newer
- *System Settings → Notifications → Gajim → Badge app icon* enabled

## Installation

### From source

```sh
make install
```

This copies the plugin to `~/.local/share/gajim/plugins/tray_indicator`
(`$XDG_DATA_HOME` is honoured). `make uninstall` removes it again.

### From archive

Build the archive with `make dist` or download `tray_indicator_<version>.zip`
from the GitHub releases, then install it in Gajim via
*Preferences → Plugins → Install from Archive*.

### Activation

New plugins are inactive by default. After installing, restart Gajim and
enable "Tray Indicator" in *Preferences → Plugins*.

## Make targets

| Target           | Description                                     |
|------------------|-------------------------------------------------|
| `make install`   | Install the plugin into the Gajim plugin folder |
| `make uninstall` | Remove the installed plugin                     |
| `make dist`      | Build `tray_indicator_<version>.zip`            |
| `make clean`     | Remove built archives and `__pycache__`         |

## Limitations

The plugin accesses Gajim internals (`app.window._chat_page`), which may
change in future Gajim versions. If the badge stops working after a Gajim
update, check *Preferences → Plugins* for an error message.

## License

MIT, see [LICENSE](LICENSE).
