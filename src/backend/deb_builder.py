#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEB Package Builder for Zorix Store
Creates installable .deb packages
"""

import os
import shutil
from pathlib import Path
import subprocess


class DebPackageBuilder:
    """Build .deb packages for Zorix Store"""
    
    @staticmethod
    def create_deb_package(app_name, package_name, version="1.0.0", description="", icon_path=None):
        """
        Create a basic .deb package structure
        
        Args:
            app_name: Human-readable app name
            package_name: Package name (lowercase, no spaces)
            version: Package version
            description: Package description
            icon_path: Path to icon file
            
        Returns:
            Path to created .deb file or None
        """
        try:
            # Create temporary build directory
            build_dir = Path("/tmp/zorix_deb_build")
            if build_dir.exists():
                shutil.rmtree(build_dir)
            build_dir.mkdir(parents=True)
            
            # Create DEBIAN metadata directory
            debian_dir = build_dir / "DEBIAN"
            debian_dir.mkdir(parents=True)
            
            # Create control file
            control_content = f"""Package: {package_name}
Version: {version}
Architecture: all
Maintainer: Zorix Store <zorix@store>
Description: {description}
Homepage: https://github.com/gabzorix/zorixstoredeb
"""
            with open(debian_dir / "control", 'w') as f:
                f.write(control_content)
            
            # Create postinst script
            postinst_content = """#!/bin/bash
set -e
echo "Package {0} installed successfully!"
exit 0
""".format(package_name)
            
            postinst_file = debian_dir / "postinst"
            with open(postinst_file, 'w') as f:
                f.write(postinst_content)
            os.chmod(postinst_file, 0o755)
            
            # Create postrm script
            postrm_content = """#!/bin/bash
set -e
echo "Package {0} removed successfully!"
exit 0
""".format(package_name)
            
            postrm_file = debian_dir / "postrm"
            with open(postrm_file, 'w') as f:
                f.write(postrm_content)
            os.chmod(postrm_file, 0o755)
            
            # Create usr/share/applications directory for desktop entry
            app_dir = build_dir / "usr" / "share" / "applications"
            app_dir.mkdir(parents=True)
            
            # Create desktop entry
            desktop_entry = f"""[Desktop Entry]
Type=Application
Name={app_name}
Comment={description}
Exec=/usr/bin/{package_name}
Icon={package_name}
Categories=Utility;
Version=1.0
"""
            
            with open(app_dir / f"{package_name}.desktop", 'w') as f:
                f.write(desktop_entry)
            
            # Copy icon if provided
            if icon_path and os.path.exists(icon_path):
                icons_dir = build_dir / "usr" / "share" / "icons" / "hicolor" / "48x48" / "apps"
                icons_dir.mkdir(parents=True)
                icon_ext = Path(icon_path).suffix
                shutil.copy2(icon_path, icons_dir / f"{package_name}{icon_ext}")
            
            # Create stub executable
            bin_dir = build_dir / "usr" / "bin"
            bin_dir.mkdir(parents=True)
            
            exec_file = bin_dir / package_name
            exec_content = f"""#!/bin/bash
echo "{app_name} v{version}"
echo "{description}"
"""
            with open(exec_file, 'w') as f:
                f.write(exec_content)
            os.chmod(exec_file, 0o755)
            
            # Build .deb package
            output_dir = Path.home() / "Downloads"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            deb_path = output_dir / f"{package_name}_{version}_all.deb"
            
            result = subprocess.run(
                ['dpkg-deb', '--build', str(build_dir), str(deb_path)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and deb_path.exists():
                # Cleanup
                shutil.rmtree(build_dir)
                return str(deb_path)
            else:
                print(f"DEB build error: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"Error building DEB: {e}")
            return None
