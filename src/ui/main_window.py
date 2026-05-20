#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zorix Store - Main UI Window
GTK4 Interface with Galactic Theme
"""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib
import threading
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from backend.package_handler import PackageHandler


# Galactic CSS Theme
GALACTIC_CSS = """
window {
    background-color: #0a0a1a;
    color: #e0e0e0;
}

headerbar {
    background: linear-gradient(90deg, #1a3a4a 0%, #2d1b4e 50%, #1a3a4a 100%);
    color: #64c8ff;
    box-shadow: 0 4px 15px rgba(100, 200, 255, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.title {
    color: #64c8ff;
    font-weight: bold;
    text-shadow: 0 0 10px rgba(100, 200, 255, 0.5);
}

searchentry {
    background-color: #1a1a3a;
    color: #64c8ff;
    border: 2px solid #64c8ff;
    box-shadow: 0 0 10px rgba(100, 200, 255, 0.3), inset 0 1px 3px rgba(0, 0, 0, 0.5);
    border-radius: 8px;
    padding: 8px;
    font-size: 14px;
}

searchentry:focus {
    background-color: #1f2a4a;
    border-color: #9d4edd;
    box-shadow: 0 0 20px rgba(157, 78, 221, 0.5), inset 0 1px 3px rgba(0, 0, 0, 0.5);
}

button {
    background: linear-gradient(135deg, #64c8ff 0%, #9d4edd 100%);
    color: #0a0a1a;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
    box-shadow: 0 4px 10px rgba(100, 200, 255, 0.2);
    border: none;
    transition: all 0.3s ease;
}

button:hover {
    background: linear-gradient(135deg, #9d4edd 0%, #64c8ff 100%);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(157, 78, 221, 0.4);
}

button:active {
    transform: translateY(0);
    box-shadow: 0 2px 10px rgba(157, 78, 221, 0.2);
}

.search-button {
    background: linear-gradient(135deg, #64c8ff 0%, #00d4ff 100%);
}

.install-button {
    background: linear-gradient(135deg, #00c853 0%, #00e680 100%);
    color: #0a0a1a;
}

.remove-button {
    background: linear-gradient(135deg, #ff1744 0%, #ff5252 100%);
    color: #fff;
}

.update-button {
    background: linear-gradient(135deg, #ffd600 0%, #ffea00 100%);
    color: #0a0a1a;
}

.list-row {
    background-color: #0a0a1a;
    color: #e0e0e0;
    border-left: 4px solid #64c8ff;
    padding: 12px;
    margin: 4px 0;
    border-radius: 4px;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.5);
}

.list-row:hover {
    background-color: #1a1a3a;
    border-left-color: #9d4edd;
    box-shadow: 0 0 10px rgba(100, 200, 255, 0.2), inset 0 1px 3px rgba(0, 0, 0, 0.5);
}

.list-row:selected {
    background-color: #2d1b4e;
    border-left-color: #64c8ff;
    box-shadow: 0 0 15px rgba(157, 78, 221, 0.3);
}

.package-name {
    color: #64c8ff;
    font-weight: bold;
    font-size: 14px;
}

.package-desc {
    color: #a0a0c0;
    font-size: 12px;
    margin-top: 4px;
}

.status-bar {
    background-color: #1a1a3a;
    color: #64c8ff;
    padding: 10px;
    border-top: 1px solid #64c8ff;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.5);
    font-size: 12px;
}

scrolledwindow {
    background-color: #0a0a1a;
}

listbox {
    background-color: #0a0a1a;
}

box {
    background-color: transparent;
}
"""


class MainWindow(Gtk.ApplicationWindow):
    """Main application window with galactic theme"""
    
    def __init__(self, app):
        """Initialize main window"""
        super().__init__(application=app)
        
        # Window properties
        self.set_title("🌌 Zorix Store - Debian Package Manager")
        self.set_default_size(900, 700)
        self.set_icon_name("package-manager")
        
        # Package handler
        self.package_handler = PackageHandler()
        self.current_packages = []
        
        # Apply CSS theme
        self._apply_theme()
        
        # Build UI
        self._build_ui()
    
    def _apply_theme(self):
        """Apply galactic CSS theme"""
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(GALACTIC_CSS.encode('utf-8'))
        
        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(
            display,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def _build_ui(self):
        """Build user interface"""
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_child(main_box)
        
        # Header bar
        header_bar = Gtk.HeaderBar()
        header_bar.set_title_widget(Gtk.Label(label="🌌 Zorix Store"))
        main_box.append(header_bar)
        
        # Content box
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_start(12)
        content_box.set_margin_end(12)
        content_box.set_margin_top(12)
        content_box.set_margin_bottom(12)
        main_box.append(content_box)
        
        # Search box
        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        content_box.append(search_box)
        
        search_entry = Gtk.SearchEntry()
        search_entry.set_placeholder_text("🔍 Search packages...")
        search_entry.set_hexpand(True)
        search_box.append(search_entry)
        
        search_button = Gtk.Button(label="🔍 Search")
        search_button.add_css_class("search-button")
        search_button.connect("clicked", self._on_search, search_entry)
        search_box.append(search_button)
        
        installed_button = Gtk.Button(label="📦 Installed")
        installed_button.connect("clicked", self._on_show_installed)
        search_box.append(installed_button)
        
        # Results label
        self.results_label = Gtk.Label()
        self.results_label.set_markup("<small>🌟 Welcome to Zorix Store! Search for packages above.</small>")
        content_box.append(self.results_label)
        
        # Scrolled window for packages
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        content_box.append(scrolled)
        
        # List box
        self.package_list = Gtk.ListBox()
        self.package_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        scrolled.set_child(self.package_list)
        
        # Action buttons box
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        content_box.append(actions_box)
        
        install_btn = Gtk.Button(label="⬇️ Install")
        install_btn.add_css_class("install-button")
        install_btn.connect("clicked", self._on_install)
        actions_box.append(install_btn)
        
        remove_btn = Gtk.Button(label="🗑️ Remove")
        remove_btn.add_css_class("remove-button")
        remove_btn.connect("clicked", self._on_remove)
        actions_box.append(remove_btn)
        
        update_btn = Gtk.Button(label="🔄 Update")
        update_btn.add_css_class("update-button")
        update_btn.connect("clicked", self._on_update)
        actions_box.append(update_btn)
        
        # Status bar
        self.status_bar = Gtk.Label()
        self.status_bar.set_markup("<small>⭐ Ready to install packages!</small>")
        self.status_bar.add_css_class("status-bar")
        self.status_bar.set_halign(Gtk.Align.START)
        main_box.append(self.status_bar)
    
    def _update_status(self, message: str):
        """Update status bar message"""
        self.status_bar.set_markup(f"<small>{message}</small>")
    
    def _populate_packages(self, packages):
        """Populate package list"""
        # Clear existing
        while True:
            row = self.package_list.get_first_child()
            if not row:
                break
            self.package_list.remove(row)
        
        self.current_packages = packages
        
        if not packages:
            self._update_status("❌ No packages found")
            return
        
        self._update_status(f"⭐ Found {len(packages)} packages")
        
        for pkg in packages:
            row = Gtk.ListBoxRow()
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            box.add_css_class("list-row")
            
            name_label = Gtk.Label()
            name_label.add_css_class("package-name")
            status = "✅ Installed" if pkg.get('installed') else "⬜ Not Installed"
            name_label.set_markup(f"{pkg['name']} <small>({status})</small>")
            name_label.set_halign(Gtk.Align.START)
            box.append(name_label)
            
            desc_label = Gtk.Label()
            desc_label.add_css_class("package-desc")
            desc_label.set_text(pkg.get('description', 'No description'))
            desc_label.set_halign(Gtk.Align.START)
            desc_label.set_wrap(True)
            desc_label.set_wrap_mode(1)
            box.append(desc_label)
            
            row.set_child(box)
            self.package_list.append(row)
    
    def _on_search(self, button, entry):
        """Handle search"""
        query = entry.get_text()
        if not query.strip():
            self._update_status("⚠️ Please enter a search query")
            return
        
        self._update_status(f"🔍 Searching for '{query}'...")
        threading.Thread(target=self._search_packages, args=(query,), daemon=True).start()
    
    def _search_packages(self, query):
        """Search packages in background"""
        packages = self.package_handler.search_packages(query)
        GLib.idle_add(self._populate_packages, packages)
    
    def _on_show_installed(self, button):
        """Show installed packages"""
        self._update_status("📦 Loading installed packages...")
        threading.Thread(target=self._load_installed, daemon=True).start()
    
    def _load_installed(self):
        """Load installed packages in background"""
        packages = self.package_handler.get_installed_packages()
        for pkg in packages:
            pkg['installed'] = True
        GLib.idle_add(self._populate_packages, packages)
    
    def _on_install(self, button):
        """Install selected package"""
        row = self.package_list.get_selected_row()
        if not row:
            self._update_status("⚠️ Please select a package")
            return
        
        pkg_name = self.current_packages[row.get_index()]['name']
        self._update_status(f"📥 Installing {pkg_name}...")
        threading.Thread(target=self._install_package, args=(pkg_name,), daemon=True).start()
    
    def _install_package(self, pkg_name):
        """Install package in background"""
        success = self.package_handler.install_package(pkg_name)
        status = f"✅ {pkg_name} installed successfully!" if success else f"❌ Failed to install {pkg_name}"
        GLib.idle_add(self._update_status, status)
    
    def _on_remove(self, button):
        """Remove selected package"""
        row = self.package_list.get_selected_row()
        if not row:
            self._update_status("⚠️ Please select a package")
            return
        
        pkg_name = self.current_packages[row.get_index()]['name']
        self._update_status(f"🗑️ Removing {pkg_name}...")
        threading.Thread(target=self._remove_package, args=(pkg_name,), daemon=True).start()
    
    def _remove_package(self, pkg_name):
        """Remove package in background"""
        success = self.package_handler.remove_package(pkg_name)
        status = f"✅ {pkg_name} removed successfully!" if success else f"❌ Failed to remove {pkg_name}"
        GLib.idle_add(self._update_status, status)
    
    def _on_update(self, button):
        """Update selected package"""
        row = self.package_list.get_selected_row()
        if not row:
            self._update_status("⚠️ Please select a package")
            return
        
        pkg_name = self.current_packages[row.get_index()]['name']
        self._update_status(f"🔄 Updating {pkg_name}...")
        threading.Thread(target=self._update_package, args=(pkg_name,), daemon=True).start()
    
    def _update_package(self, pkg_name):
        """Update package in background"""
        success = self.package_handler.update_package(pkg_name)
        status = f"✅ {pkg_name} updated successfully!" if success else f"❌ Failed to update {pkg_name}"
        GLib.idle_add(self._update_status, status)
