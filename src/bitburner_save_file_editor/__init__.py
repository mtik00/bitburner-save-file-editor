from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Header, Footer, Static
from bitburner_save_file_editor.save import SaveGame
from pathlib import Path
import sys

import argparse
def parse_args(args: list[str] = sys.argv[1:]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-d", "--directory", help="Game save directory to search")
    group.add_argument("-f", "--file", help="The save game file to modify")

    return parser.parse_args(args)


class ButtonApp(App):
    """A simple Textual app with 5 buttons."""
    
    CSS = """
    Screen {
        align: center middle;
    }
    
    Vertical {
        width: 50;
        height: auto;
        background: $surface;
        padding: 2;
        border: solid $primary;
    }
    
    Button {
        width: 100%;
        margin: 1;
    }
    
    #status {
        height: 3;
        content-align: center middle;
        margin: 1;
        color: $text;
    }
    """
    
    BINDINGS = [("q", "quit", "Quit")]
    
    def __init__(self, gzip_file: Path):
        """Initialize the app with an optional JSON file path."""
        super().__init__()

        self.infile = gzip_file
        self.savegame = SaveGame(gzip_file)
        self.outfile = self.savegame.outfile
 
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Vertical():
            yield Static(f"in file: {self.infile.stem}")
            yield Static(f"out file: {self.outfile.stem}")
            yield Static("Click any button to perform an action", id="status")
            yield Button(f"Set player money to 5Q from {self.savegame.money:.2e}", id="money", variant="primary")
            yield Button("Set player hack exprience to 14000", id="hack", variant="primary")
            yield Button("Add 5M faction rep", id="factions", variant="primary")
            yield Button("All of the above", id="all", variant="primary")
            yield Button("Exit", id="exit", variant="success")
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        button_id = event.button.id
        status = self.query_one("#status", Static)
        
        if button_id == "exit":
            self.exit()
        elif button_id == "money":
            self.savegame.money = 5E20
            self.savegame.save()
            self.savegame.load()
            status.update("Money updated!")
        elif button_id == "hack":
            self.savegame.hack_exp = int(1E100)
            self.savegame.save()
            self.savegame.load()
            status.update("Hacking experience updated!")
        elif button_id == "factions":
            self.savegame.set_factions()
            self.savegame.save()
            self.savegame.load()
            status.update("All factions unlocked!")
        elif button_id == "all":
            self.savegame.money = 5E20
            self.savegame.hack_exp = int(1E100)
            self.savegame.set_factions()
            self.savegame.save()
            self.savegame.load()
            status.update("All hacks applied!")
        else:
            # Update status message for action buttons
            status.update(f"You clicked Action {button_id}!")

def get_file(directory: str | None, file: str | None) -> Path:
    if file:
        return Path(file)
    
    assert isinstance(directory, str)
    files = sorted([x for x in Path(directory).glob("bitburnerSave*.json.gz")], reverse=True)

    if not files:
        raise ValueError(f"Could not find bitburnerSave file in {directory}")
    
    return files[0]

def main():
    args = parse_args()
    if not (args.directory or args.file):
        print("ERROR: must define either --file or --directory")
        return

    gzip_file = get_file(args.directory, args.file)

    app = ButtonApp(gzip_file)
    app.run()


if __name__ == "__main__":
    main()
