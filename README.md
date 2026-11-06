
![sealion_logotype_256_alpha](https://github.com/wicknix/SeaLion/assets/39230578/91143f53-c942-40ed-b5f8-7cb752ab9187)

A web browser for Intel MacOS 10.7 - 14.8, Linux, and 64-bit Windows.

Original source: https://github.com/wicknix/SeaLion

Built upon the [unified XUL platform](https://repo.palemoon.org/MoonchildProductions/UXP).

What features are included
=========================================================================

* Tabbed Browsing
* Comprehensive control of Preferences
* Customizable Toolbars
* XUL Overlay and Bootstrap Extension Support
* SeaMonkey Theme Support
* Supports Plug-ins
* Supports the JXL image format
* Supports Flash
* Supports 'dark mode' on supported sites (set via preferences pane)
* Ability to switch profiles
* Multiple Search Engine Providers built in
* Built upon a mature and secure code base
* Privacy respecting. Doesn't 'phone home' like many 'popular' browsers do

What is not included
=========================================================================

* Digital Rights Management (DRM) such as Encrypted Media Extensions (EME)
* WebRTC
* WebExtensions
* Developer tools (some functionality can be added back via an extension)
* Lightweight Themes/Toolbar Backgrounds
* Language Packs (English only)
* The full suite. If you want that check out [BrassMonkey](https://github.com/wicknix/brass-monkey)
* A Windows installer. 64-bit Windows builds and runs from `dist\bin`; see below. There is no NSIS setup program.


Building on 64-bit Windows
=========================================================================

The checked-in `.mozconfig` is still the macOS cross-compile setup. On Windows, build from the repository root with `win-mach.cmd`. It picks `.mozconfig-windows`, prefers MozillaBuild's Python 3, and follows the directory the script lives in, so another checkout path works without editing the script.

`win-mach.cmd` looks for MozillaBuild in `MOZILLABUILD`, then `C:\mozilla-build`. The source path must not contain spaces.

```
win-mach.cmd clobber
win-mach.cmd build
win-mach.cmd /mozillabuild D:\mozilla-build build
```

What this machine used successfully:

* MozillaBuild 3.4
* Visual Studio 18 Community (MSVC 14.51) and Windows SDK 10.0.28000.0
* UXP tag `RB_20260602` (the 2026-06-02 release named by SeaLion 34.3.0) checked out into `platform/`

The official UXP URLs were not reachable from here (`github.com/MoonchildProductions/UXP` is missing, and `repo.palemoon.org` redirects offline). The tree that built is the FranklinDM mirror:

```
git clone --depth 1 --branch RB_20260602 https://github.com/FranklinDM/UXP.git platform
```

The `vswhere.exe` shipped in that UXP tag does not see Visual Studio 18. Configure found the compiler after replacing `platform/build/win32/vswhere.exe` with a newer `vswhere` (3.1.7 from the Visual Studio installer). `client.mk` also refuses a MinGW build when it contains Windows CR line endings; the application tree needs LF.

Quit SeaLion before `clobber`. A running `sealion.exe` locks files in the object directory and the delete fails.

The program is `obj-x86_64-pc-mingw32\dist\bin\sealion.exe`. That file is only the launcher. Keep the whole `dist\bin` directory with it (`xul.dll` and the rest of the runtime). `win-mach.cmd package` does not produce a zip: packaging still expects `bin/uninstall/helper.exe`, and `navigator/installer/windows` is not part of this tree.

Available Extensions for SeaLion
======================
* adblock latitude - ad blocker
* bbcodextra - adds custom tag commands to context menu
* bluehell firewall - ad blocker
* chatzilla - irc client
* cookies exterminator - auto deletes cookies
* copy as plain text - copies text w/out formatting
* dom inspector - inspects the structure and properties of a window
* dorando keyconfig - rebind your keys
* download status bar - powerful download manager
* down them all - media downloader
* email this - adds context menu to 'email this'
* ematrix - port of umatrix that blocks scripts, ads, etc
* fireftp - ftp client
* fireshot - take screen shots of web pages
* greasemonkey - user script manager
* hit a hint - open links with keyboard shortcuts
* https always - encrypt the web
* menu wizard - customize your browsers menus
* modhresponse - rewrite http response
* mouse gestures suite - scroll wheel navigation, page scrolling, tab scrolling
* multiple tab handler - manage your tabs
* nicereader - similar to readerview
* overbiteff - enables the gopher protocol
* page navigation buttons - adds a few buttons to help with page navigation
* palefill - injects polyfills for various web technologies
* password backup tool - imports and exports passwords to/from .csv
* pdf-js - html5 pdf reader
* private tab - opens a private browsing tab
* quicknote - notes extension with advanced features
* quick passwords - quickly login and get passwords
* seatab - adds a close button to each tab
* secret-agent - enhances the privacy of your web surfing
* swarth - psuedo dark mode extension 
* tab clicking options - assign tab related actions to clicking events
* torrent tornado - torrent client
* uBlock0rigin - ad blocker
* user agent switcher - self explanitory
* web developer - adds some extra easy to access functions
* website navigation bar - reintroduces SeaMonkeys navigation bar
* world ip - geo add-on with security features and advanced network tools

* **All the extensions listed above are found in the SeaLion-Extras.zip**

Available Extra Themes for SeaLion
======================
* kilome
* modern2
* orthodox
* pinball
* littlemonkey
* gnomerunner (linux only)

You can also drag your extension icons to the component bar (lower left) instead of having them on the tool bar for a cleaner look.
![component-bar](https://github.com/wicknix/SeaLion/assets/39230578/946a5dac-dbf6-421b-b871-48056dc34621)

GnomeRunner Linux theme - Uses GTK theme style and icons
![gnomerunner-theme-linux](https://github.com/wicknix/SeaLion/assets/39230578/37e3a277-9918-4681-984f-50f2651b0747)

The 'default theme' even though on first start it will use Gray Modern by default
![SL-default-theme](https://github.com/wicknix/SeaLion/assets/39230578/5aa88392-c5e5-4646-a18d-e57a6bbee974)

PowerPC Linux build is compatible with 32-bit Debian 12 / Fienix 6 / MintPPC
![sealion-powerpc-about](https://github.com/wicknix/SeaLion/assets/39230578/84c5a83c-c174-4340-9e46-b99c32410d31)


