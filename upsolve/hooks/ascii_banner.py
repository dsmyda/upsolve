from ..core.version import get_version

def show_ascii_banner(app):
    print("""

 /$$   /$$                               /$$
| $$  | $$                              | $$
| $$  | $$  /$$$$$$   /$$$$$$$  /$$$$$$ | $$ /$$    /$$ /$$$$$$
| $$  | $$ /$$__  $$ /$$_____/ /$$__  $$| $$|  $$  /$$//$$__  $$
| $$  | $$| $$  \ $$|  $$$$$$ | $$  \ $$| $$ \  $$/$$/| $$$$$$$$
| $$  | $$| $$  | $$ \____  $$| $$  | $$| $$  \  $$$/ | $$_____/
|  $$$$$$/| $$$$$$$/ /$$$$$$$/|  $$$$$$/| $$   \  $/  |  $$$$$$$
 \______/ | $$____/ |_______/  \______/ |__/    \_/    \_______/
          | $$
          | $$                                        CLI v%s
          |__/                                 created by dsmyda

          """ % get_version())