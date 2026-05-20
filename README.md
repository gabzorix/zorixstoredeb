# 🌌 Zorix Store - Debian Package Manager

A modern, galactic-themed application store for Debian systems with a sleek GTK4 interface.

## 🎨 Features

- ✨ **Galactic Theme**: Dark cosmic design with blue, purple, and indigo gradients
- 🔍 **Package Search**: Search APT repositories for packages
- 📦 **Package Management**: Install, remove, and update packages
- 👁️ **Installed Packages**: View all installed packages on your system
- 🚀 **Modern UI**: GTK4 interface with smooth animations and effects
- ⭐ **Beautiful Icon**: Cosmic "Z" logo with glow effects

## 🌟 Design

The Zorix Store features a futuristic galactic design with:
- **Colors**: Deep space black (#0a0a1a), cosmic blue (#64c8ff), cosmic purple (#9d4edd)
- **Effects**: Glowing shadows, smooth transitions, cosmic particles
- **Icon**: Stylized "Z" with radial gradient and celestial decoration

## 📋 Requirements

- Python 3.8+
- GTK 4.0+
- APT package manager (Debian/Ubuntu)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/gabzorix/zorixstoredeb.git
cd zorixstoredeb
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make the main script executable:
```bash
chmod +x main.py
```

## 🚀 Usage

Run the application:
```bash
python3 main.py
```

### Features:

- **🔍 Search**: Enter a package name in the search box and click "Search"
- **📥 Install**: Select a package and click "⬇️ Install" (requires sudo)
- **🗑️ Remove**: Select an installed package and click "🗑️ Remove" (requires sudo)
- **🔄 Update**: Update an installed package to the latest version (requires sudo)
- **📦 View Installed**: Click "📦 Installed" to see all installed packages

## 🎯 Project Structure

```
zorixstoredeb/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── src/
│   ├── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── main_window.py          # GTK4 UI window with galactic theme
│   └── backend/
│       ├── __init__.py
│       └── package_handler.py      # Debian package management
└── assets/
    └── icons/
        └── zorix-z.svg             # Cosmic Z logo
```

## 🛠️ Development

### Adding New Features

1. **UI Components**: Edit `src/ui/main_window.py`
2. **Package Operations**: Edit `src/backend/package_handler.py`
3. **Styling**: Modify the `GALACTIC_CSS` in `src/ui/main_window.py`

### Building Custom Packages

The application uses APT/DEB package format. You can:
- Package your own applications as .deb files
- Add custom repositories
- Create custom package managers

## 📝 License

This project is open source and available under the MIT License.

## 🌍 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📧 Contact

For questions or suggestions, open an issue on GitHub.

---

**Made with ❤️ by Zorix - Bringing Galactic Design to Package Management** 🚀✨
