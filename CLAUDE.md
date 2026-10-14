# CLAUDE.md

Gajim plugin (macOS only) that sets the unread message count as Dock badge.
Usage and installation: see README.md.

## Gajim reference

- Gajim sources of the installed app: `/Applications/Gajim.app/Contents/Resources/gajim/`
  (Gajim 2.6.0 at time of writing). Check there before relying on internals.
- PyObjC (`AppKit`) is bundled; Gajim itself uses it in `gtk/sound.py`.
- Gajim has no tray icon on macOS: `gtk/tray_icon.py` uses `NoneBackend` for `darwin`.

## Plugin loading pitfalls

- `tray_indicator/__init__.py` must only import the plugin class. The loader
  (`plugins/pluginmanager.py`, `_load_plugin_module`) calls `issubclass()` on
  every module attribute in `dir()` order.
- The plugin directory name is used as module name.
- Plugins are activated before the main window exists, hence the polling
  until `app.window` is set.
- Newly installed plugins are inactive (`PLUGIN_SETTINGS = {"active": False}`).
- ZIP archives need an explicit top-level directory entry (`tray_indicator/`);
  `make dist` creates it.

## Gajim internals in use

- `app.window._chat_page.get_chat_list_stack()` (private)
- `ChatListStack` signal `unread-count-changed` and `get_total_unread_count()`

Verify these first after a Gajim update.

## Testing

Outside Gajim only a syntax check is possible (`python3 -I -m py_compile`).
Real test: `make install`, restart Gajim, enable the plugin in
*Preferences → Plugins*.

## Release

- Bump `version` in `tray_indicator/plugin-manifest.json`.
- Tag = version without `v` prefix (e.g. `0.1.0`), annotated.
- `make dist`, then `gh release create <version> tray_indicator_<version>.zip --verify-tag`.
- Commit email is set repo-locally (`git config --local user.email`).
