from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Digits, Footer, Header, Input, Label, Select

ALPH = [
    "Binary:01",
    "Octal:01234567",
    "Decimal:0123456789",
    "Hexadecimal:0123456789ABCDEF",
    "Base 26 (A-Z):ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "Base 27 (A-Z, space):ABCDEFGHIJKLMNOPQRSTUVWXYZ ",
    "Base 36 (0-9, A-Z):0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "Base 37 (0-9, A-Z, space):0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ ",
    "Base 62 (0-9, A-Z, a-z):0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    "Base 63 (0-9, A-Z, a-z, space):0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ",
    "Custom:Custom Alphabet",
]

class BaseConversionApp(App):
    """A simple base conversion application."""

    CSS = """
    Horizontal {
        align-horizontal: center;
        height: auto;
        margin-top: 1;
    }
    Button {
        width: 1fr;
        margin: 0 2;
    }
    #result_output {
        margin-top: 1;
        border: round $primary;
        height: 5;
        content-align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        options = [tuple(item.split(":", 1)) for item in ALPH]
        yield Header("Base Conversion App")
        yield Input(id="number_input", placeholder="Enter a number in the original format (e.g., 10.5, 2.AF3)")
        yield Label("Input alphabet:")
        yield Select(options, id="base_input")
        yield Input(id="custom_alphabet_input", placeholder="Enter input custom alphabet")
        yield Label("Output alphabet:")
        yield Select(options, id="base_output")
        yield Input(id="custom_alphabet_output", placeholder="Enter output custom alphabet")
        with Horizontal():
            yield Button("Convert", variant="primary", id="convert")
            yield Button("Clear", id="clear")
        yield Digits("", id="result_output")
        yield Button("Exit", variant="error", id="exit")

    def on_mount(self):
        """Hide the custom input fields on startup."""
        self.query_one("#custom_alphabet_input").display = False
        self.query_one("#custom_alphabet_output").display = False
    
    @on(Select.Changed)
    def on_select_changed(self, event: Select.Changed):
        custom_alph_id = f"#custom_alphabet_{'input' if event.select.id == 'base_input' else 'output'}"
        custom_alph = self.query_one(custom_alph_id, Input)
        is_custom = event.value == "Custom Alphabet"
        custom_alph.display = is_custom
        if is_custom:
            custom_alph.focus()

if __name__ == "__main__":
    app = BaseConversionApp()
    app.run()