import os
from rich import print

folder_path = os.path.expanduser("~/.visionai")

if not os.path.exists(folder_path):
    print("[bold red] Visionai config folder not found please create [bold yellow].visionai[/bold yellow] folder in home directory and paste [bold yellow].env[/bold yellow] file before do visionai init[/bold red]")

