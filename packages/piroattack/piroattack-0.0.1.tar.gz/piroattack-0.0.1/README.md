# PiroAttack 🔒

![License](https://img.shields.io/github/license/hk4crprasad/PiroAttack) ![PyPI Version](https://img.shields.io/pypi/v/piroattack) ![GitHub Stars](https://img.shields.io/github/stars/hk4crprasad/PiroAttack?style=social)

**⚠️ THIS PROJECT IS NO LONGER MAINTAINED ⚠️**

PiroAttack is a Python 3 app designed for **SECURITY TESTING PURPOSES ONLY!** 🛡️ It leverages the HTTP Keep Alive + NoCache attack vector for HTTP DoS testing.

## Installation

```bash
pip install piroattack
```

## Usage

```bash
piroattack <url> [OPTIONS]
```

### Options:

- `-u, --useragents`  File with user-agents to use (default: randomly generated)
- `-w, --workers`     Number of concurrent workers (default: 50)
- `-s, --sockets`     Number of concurrent sockets (default: 30)
- `-m, --method`      HTTP Method to use 'get' or 'post' or 'random' (default: get)
- `-d, --debug`       Enable Debug Mode [more verbose output] (default: False)
- `-n, --nosslcheck`  Do not verify SSL Certificate (default: True)
- `-h, --help`        Shows this help

## Utilities

- **util/getuas.py** - Fetches user-agent lists from [useragentstring.com](http://www.useragentstring.com/pages/useragentstring.php) subpages. (*REQUIRES BEAUTIFULSOUP4*)
- **res/lists/useragents** - Text lists (one per line) of User-Agent strings (from [useragentstring.com](http://www.useragentstring.com))

## Changelog 📆

- **2016-02-06:** Added support for not verifying SSL Certificates
- **2014-02-20:** Added randomly created user agents (still RFC compliant).
- **2014-02-19:** Removed silly referers and user agents. Improved randomness of referers. Added external user-agent list support.
- **2013-03-26:** Changed from threading to multiprocessing. Still has some bugs to resolve like I still don't know how to properly shut down the manager.
- **2012-12-09:** Initial release

## To-do 📝

- Change from getopt to argparse
- Change from string.format() to printf-like

## License 📜

This software is distributed under the GNU General Public License version 3 (GPLv3).

## LEGAL NOTICE ⚖️

THIS SOFTWARE IS PROVIDED FOR EDUCATIONAL USE ONLY! IF YOU ENGAGE IN ANY ILLEGAL ACTIVITY, THE AUTHOR DOES NOT TAKE ANY RESPONSIBILITY FOR IT. BY USING THIS SOFTWARE, YOU AGREE WITH THESE TERMS.

🚀 **Author:** [HK4CRPRASAD](https://github.com/hk4crprasad)
📬 **Telegram:** [t.me/hk4crprasad](https://t.me/hk4crprasad)