#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zorix Store - Package Handler
Debian/APT Package Management Backend
"""

import subprocess
import json
from typing import List, Dict, Optional


class PackageHandler:
    """Handle Debian package operations via APT"""
    
    def __init__(self):
        """Initialize package handler"""
        self.cache = {}
    
    def search_packages(self, query: str) -> List[Dict[str, str]]:
        """
        Search for packages in APT repositories
        
        Args:
            query: Package search query
            
        Returns:
            List of package information dictionaries
        """
        try:
            result = subprocess.run(
                ['apt-cache', 'search', query],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            packages = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split(' - ', 1)
                    if len(parts) == 2:
                        name = parts[0].strip()
                        description = parts[1].strip()
                        packages.append({
                            'name': name,
                            'description': description,
                            'installed': self.is_installed(name)
                        })
            
            return packages
        except Exception as e:
            print(f"Error searching packages: {e}")
            return []
    
    def get_installed_packages(self) -> List[Dict[str, str]]:
        """
        Get list of installed packages
        
        Returns:
            List of installed package information
        """
        try:
            result = subprocess.run(
                ['dpkg', '-l'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            packages = []
            for line in result.stdout.strip().split('\n')[5:]:  # Skip header
                if line.startswith('ii'):
                    parts = line.split()
                    if len(parts) >= 4:
                        packages.append({
                            'name': parts[1],
                            'version': parts[2],
                            'arch': parts[3],
                            'status': 'installed'
                        })
            
            return packages
        except Exception as e:
            print(f"Error getting installed packages: {e}")
            return []
    
    def is_installed(self, package_name: str) -> bool:
        """
        Check if package is installed
        
        Args:
            package_name: Name of the package
            
        Returns:
            True if installed, False otherwise
        """
        try:
            result = subprocess.run(
                ['dpkg', '-l', package_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def get_package_info(self, package_name: str) -> Optional[Dict]:
        """
        Get detailed package information
        
        Args:
            package_name: Name of the package
            
        Returns:
            Package information dictionary or None
        """
        try:
            result = subprocess.run(
                ['apt-cache', 'show', package_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            info = {}
            for line in result.stdout.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()
            
            return info if info else None
        except Exception as e:
            print(f"Error getting package info: {e}")
            return None
    
    def install_package(self, package_name: str) -> bool:
        """
        Install a package (requires sudo)
        
        Args:
            package_name: Name of the package to install
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = subprocess.run(
                ['sudo', 'apt-get', 'install', '-y', package_name],
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error installing package: {e}")
            return False
    
    def remove_package(self, package_name: str) -> bool:
        """
        Remove a package (requires sudo)
        
        Args:
            package_name: Name of the package to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = subprocess.run(
                ['sudo', 'apt-get', 'remove', '-y', package_name],
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error removing package: {e}")
            return False
    
    def update_package(self, package_name: str) -> bool:
        """
        Update a package (requires sudo)
        
        Args:
            package_name: Name of the package to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = subprocess.run(
                ['sudo', 'apt-get', 'upgrade', '-y', package_name],
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error updating package: {e}")
            return False
    
    def update_package_lists(self) -> bool:
        """
        Update package lists (requires sudo)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            result = subprocess.run(
                ['sudo', 'apt-get', 'update'],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error updating package lists: {e}")
            return False
