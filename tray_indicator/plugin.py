from __future__ import annotations

from typing import Any

import logging

from AppKit import NSApplication
from gi.repository import GLib

from gajim.common import app
from gajim.gtk.chat_list_stack import ChatListStack
from gajim.plugins import GajimPlugin

log = logging.getLogger("gajim.p.tray_indicator")


class TrayIndicatorPlugin(GajimPlugin):
    def init(self) -> None:
        self._chat_list_stack: ChatListStack | None = None
        self._handler_id: int | None = None
        self._source_id: int | None = None

    def activate(self) -> None:
        # Plugins are activated before the main window exists
        if self._try_connect():
            self._source_id = GLib.timeout_add(500, self._try_connect)

    def deactivate(self) -> None:
        if self._source_id is not None:
            GLib.source_remove(self._source_id)
            self._source_id = None

        if self._chat_list_stack is not None and self._handler_id is not None:
            self._chat_list_stack.disconnect(self._handler_id)
        self._chat_list_stack = None
        self._handler_id = None

        self._set_badge(0)

    def _try_connect(self) -> bool:
        if app.window is None:
            return GLib.SOURCE_CONTINUE

        self._source_id = None
        self._chat_list_stack = app.window._chat_page.get_chat_list_stack()
        self._handler_id = self._chat_list_stack.connect(
            "unread-count-changed", self._on_unread_count_changed
        )
        self._update_badge()
        return GLib.SOURCE_REMOVE

    def _on_unread_count_changed(self, *args: Any) -> None:
        self._update_badge()

    def _update_badge(self) -> None:
        assert self._chat_list_stack is not None
        self._set_badge(self._chat_list_stack.get_total_unread_count())

    @staticmethod
    def _set_badge(count: int) -> None:
        label = str(count) if count > 0 else None
        log.debug("Set dock badge: %s", label)
        NSApplication.sharedApplication().dockTile().setBadgeLabel_(label)
