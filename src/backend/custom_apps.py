#!/usr/bin/env python3
# Custom Apps Manager Backend
import json, os, shutil
from pathlib import Path

class CustomAppsManager:
    def __init__(self):
        self.apps_dir = Path.home() / ".zorix_store" / "apps"
        self.apps_dir.mkdir(parents=True, exist_ok=True)
        self.apps_file = self.apps_dir / "apps.json"
        self.icons_dir = self.apps_dir / "icons"
        self.icons_dir.mkdir(parents=True, exist_ok=True)
        self.apps = self._load_apps()
    
    def _load_apps(self):
        if self.apps_file.exists():
            try:
                with open(self.apps_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_apps(self):
        with open(self.apps_file, 'w', encoding='utf-8') as f:
            json.dump(self.apps, f, indent=2, ensure_ascii=False)
    
    def add_app(self, name, description, package, icon_path=None):
        for app in self.apps:
            if app['package'] == package:
                return False
        app_entry = {'name': name, 'description': description, 'package': package, 'icon': None, 'type': 'custom'}
        if icon_path and os.path.exists(icon_path):
            icon_filename = f"{package}_icon.png"
            icon_dest = self.icons_dir / icon_filename
            shutil.copy2(icon_path, icon_dest)
            app_entry['icon'] = str(icon_dest)
        self.apps.append(app_entry)
        self._save_apps()
        return True
    
    def get_all_apps(self):
        return self.apps
    
    def remove_app(self, package):
        for i, app in enumerate(self.apps):
            if app['package'] == package:
                if app.get('icon') and os.path.exists(app['icon']):
                    os.remove(app['icon'])
                self.apps.pop(i)
                self._save_apps()
                return True
        return False
