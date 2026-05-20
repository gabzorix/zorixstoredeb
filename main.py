#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zorix Store - Debian Package Manager
A modern galactic-themed app store for Debian systems
"""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from ui.main_window import MainWindow


def main():
    """Main entry point for Zorix Store"""
    app = Gtk.Application(application_id='com.zorix.store')
    app.connect('activate', on_activate)
    return app.run(sys.argv)


def on_activate(app):
    """Handle application activation"""
    win = MainWindow(app)
    win.present()


if __name__ == '__main__':
    sys.exit(main())
