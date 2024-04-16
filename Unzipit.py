import subprocess
import sys
from importlib.metadata import version, PackageNotFoundError
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import json
from pathlib import Path
import zipfile

def check_and_install_dependencies():
    required_packages = {
        'rich': '9.13.0'
    }
    
    for package, min_version in required_packages.items():
        try:
            installed_version = version(package)
            if installed_version < min_version:
                raise PackageNotFoundError
        except PackageNotFoundError:
            print(f"Installing or upgrading required package: {package} (>= {min_version})")
            subprocess.check_call([sys.executable, "-m", "pip", "install", f"{package}>={min_version}"])

def main():
    check_and_install_dependencies()

    def load_translations(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def unzip_files(source_dir, destination_dir, translations, lang):
        source_dir = Path(source_dir)
        destination_dir = Path(destination_dir)

        if not source_dir.exists():
            console.print(translations[lang]['source_not_exist'], style="bold red")
            return
        if not destination_dir.exists():
            console.print(translations[lang]['destination_not_exist'], style="bold red")
            destination_dir.mkdir(parents=True, exist_ok=True)
            console.print(translations[lang]['destination_created'].format(destination_dir), style="green")

        zip_files = list(source_dir.rglob('*.zip'))
        if not zip_files:
            console.print(translations[lang]['no_zip_found'], style="bold red")
            return

        for zip_file in zip_files:
            full_path = zip_file.absolute()
            console.print(translations[lang]['extracting'].format(full_path, destination_dir), style="yellow")
            with zipfile.ZipFile(full_path, 'r') as zip_ref:
                zip_ref.extractall(destination_dir)

        console.print(translations[lang]['extraction_complete'], style="bold green")

    console = Console()
    translations = load_translations('translations.json')

    # ASCII Art Logo
    logo = """
     __    __                      __            ______  ________ 
    |  \\  |  \\                    |  \\          |      \\|        \\
    | $$  | $$ _______   ________  \\$$  ______   \\$$$$$$ \\$$$$$$$$
    | $$  | $$|       \\ |        \\|  \\ /      \\   | $$     | $$   
    | $$  | $$| $$$$$$$\\ \\$$$$$$$$| $$|  $$$$$$\\  | $$     | $$   
    | $$  | $$| $$  | $$  /    $$ | $$| $$  | $$  | $$     | $$   
    | $$__/ $$| $$  | $$ /  $$$$_ | $$| $$__/ $$ _| $$_    | $$   
     \\$$    $$| $$  | $$|  $$    \\| $$| $$    $$|   $$ \\   | $$   
      \\$$$$$$  \\$$   \\$$ \\$$$$$$$$ \\$$| $$$$$$$  \\$$$$$$    \\$$   
                                      | $$                        
                                      | $$                        
                                       \\$$                        
    """
    console.print(Panel(logo, title="[bold blue]UnzipIT[/bold blue]", subtitle="Unzip files easily", expand=False))
    console.print("This program helps you to unzip files within a directory and its subdirectories.\n", style="italic")

    lang_choice = Prompt.ask("Choose your language", choices=list(translations.keys()), default="en")
    source_directory = Prompt.ask(translations[lang_choice]['source_prompt'])
    destination_directory = Prompt.ask(translations[lang_choice]['destination_prompt'])

    unzip_files(source_directory, destination_directory, translations, lang_choice)

if __name__ == "__main__":
    main()
