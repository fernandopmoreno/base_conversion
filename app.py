from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Header, Input, Label, Select
from conversion import base_convert

from alphs import ALPH

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
    #result_label {
        width: 100%;
        margin-top: 1;
        height: 5;
        content-align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        options = [tuple(item.split(":", 1)) for item in ALPH]
        yield Header("Base Conversion App")
        yield Input(id="number_input", placeholder="Enter a number in the original format (e.g., 10.5, 2.AF3)")
        yield Select(options, id="base_input", prompt="Select input alpahabet")
        yield Input(id="custom_alphabet_input", placeholder="Enter input custom alphabet")
        yield Select(options, id="base_output", prompt="Select output alphabet")
        yield Input(id="custom_alphabet_output", placeholder="Enter output custom alphabet")
        with Horizontal():
            yield Button("Convert", variant="primary", id="convert")
            yield Button("Clear", id="clear")
        yield Label("", id="result_label", classes="result-label")
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

    @on(Button.Pressed, "#convert")
    def convert_number(self):
        number_input = self.get_number_input()
        alph_input = self.alph_selection("input")
        alph_output = self.alph_selection("output")
        if not number_input or not alph_input or not alph_output:
            return
        if not self.input_in_alph(alph_input, number_input):
            self.query_one("#result_label", Label).update("Invalid input in the selected alphabet")
            return
        try:
            number_output = base_convert(alph_input, alph_output, number_input)
            self.query_one("#result_label", Label).update(number_output)
        except Exception as e:
            self.query_one("#result_label", Label).update(f"Error during conversion: {e}")

    @on(Button.Pressed, "#clear")
    def clear_input(self):
        self.query_one("#number_input", Input).value = ""
        self.query_one("#result_label", Label).update("")

    @on(Button.Pressed, "#exit")
    def exit_app(self):
        self.exit()

    def get_number_input(self):
        input_widget = self.query_one("#number_input", Input)
        if not input_widget.value:
            self.query_one("#result_label", Label).update("Please enter a number")
            return None
        return input_widget.value

    def alph_selection(self, part):
        if self.query_one(f"#custom_alphabet_{part}", Input).display:
            alph = self.query_one(f"#custom_alphabet_{part}", Input).value
        else:
            alph = self.query_one(f"#base_{part}", Select).value
        if not alph:
            self.query_one("#result_label", Label).update("Please select valid alphabets")
            return None
        return alph

    def input_in_alph(self, alph, number):
        for char in number:
            if char not in alph + ".":
                return False
        return True