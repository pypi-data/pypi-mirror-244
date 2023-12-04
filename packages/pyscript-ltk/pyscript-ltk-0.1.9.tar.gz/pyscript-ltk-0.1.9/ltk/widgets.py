# LTK - Copyright 2023 - All Rights Reserved - chrislaffra.com - See LICENSE 

from pyscript import window # type: ignore
from ltk.jquery import *

__all__ = [
    "HBox", "Div", "VBox", "Container", "Card", "Preformatted", "Text", "Input", "Checkbox",
    "Label", "Button", "Link", "Strong", "Important", "Italic", "Paragraph", "Break", "Heading1",
    "Heading2", "Heading3", "Heading4", "OrderedList", "UnorderedList", "ListItem", "Span",
    "Tabs", "File", "DatePicker", "ColorPicker", "RadioGroup", "RadioButton", "Table", "TableRow",
    "TableHeader", "TableData", "VerticalSplitPane", "TextArea", "Code", "Image", "MenuBar", "Switch",
    "MenuLabel", "Menu", "Popup", "MenuPopup", "MenuItem", "Select", "Option", "Widget", "callback"
]

BROWSER_SHORTCUTS = [ "Cmd+N","Cmd+T","Cmd+W", "Cmd+Q" ]
DEFAULT_CSS = {}
shortcuts = {}
timers = {}


def callback(function):
    def inner(*args, **argv):
        return function(*args, **argv)
    return proxy(inner)


class Widget(object):
    """Base class for LTK widgets."""
    classes = []
    instances = {}
    element = None
    tag = "div"

    def __init__(self, *args):
        """
        Initializes a new Widget instance.

        Args:
            *args: The content to add to this widget. Can be other widgets, strings, lists, etc.

        Sets:
            self.element: The jQuery element representing this widget.
        """
        self.element = (
            jQuery(f"<{self.tag}>")
                .addClass(" ".join(self.classes))
                .append(*self._flatten(args))
        )
        self._handle_css(args)

    def _handle_css(self, args):
        """Apply CSS styles passed in the args to the widget.

        Iterates through the args and checks for any that are dicts, 
        treating them as CSS style definitions to apply to the widget.
        """
        for arg in filter(lambda arg: isinstance(arg, dict), args):
            for key, value in arg.items():
                self.css(key, value)

    def _flatten(self, children):
        """Flatten a list of child widgets into a flat list.

        Arguments:
            children (list): A list of child widgets.
            Each child can be a Widget, a jQuery element. 
            Also allowed is a list or a generator of widgets.
            Finally, if one of the children is a dict, it is used to set CSS values on the receiver

        Returns:
            list: A flat list containing the child widgets and any
                grandchildren widgets.
        """
        result = []
        for child in children:
            if isinstance(child, dict):
                continue
            elif isinstance(child, Widget):
                result.append(child.element)
            elif type(child).__name__ == "generator":
                result.extend(self._flatten(child))
            elif isinstance(child, list):
                result.extend(self._flatten(child))
            elif isinstance(child, float):
                result.append(str(child))
            else:
                result.append(child)
        return result

    def __getattr__(self, name):
        try:
            return getattr(self.element, name)
        except AttributeError as e:
            raise AttributeError(f"Cannot find attribute '{name}' in the LTK widget {self}, nor in its jQuery element")

    def left(self, value=None):
        return self.css("left", value) if value != None else self.css("left")

    def right(self, value=None):
        return self.css("right", value) if value != None else self.css("right")

    def top(self, value=None):
        return self.css("top", value) if value != None else self.css("top")

    def bottom(self, value=None):
        return self.css("bottom", value) if value != None else self.css("bottom")

    def opacity(self, value=None):
        return self.css("opacity", value) if value != None else self.css("opacity")

    def display(self, value=None):
        return self.css("display", value) if value != None else self.css("display")

    def position(self, value=None):
        return self.css("position", value) if value != None else self.css("position")

    def border(self, value=None):
        return self.css("border", value) if value != None else self.css("border")


class HBox(Widget):
    """ Lays out its child widgets horizontally """
    classes = [ "ltk-hbox" ]


class Div(Widget):
    """ Wraps an HTML element of type <div> """
    classes = [ "ltk-div" ]



class VBox(Widget):
    """ Lays out its child widgets vertically """
    classes = [ "ltk-vbox" ]


class Container(Widget):
    """ Wraps an HTML element of type <div> """
    classes = [ "ltk-container" ]


class Card(Container):
    """ A container with special styling looking like a card """
    classes = [ "ltk-card" ]


class Preformatted(Widget):
    """ Wraps an HTML element of type <pre> """
    classes = [ "ltk-pre" ]
    tag = "pre"


class Text(Widget):
    """ A <div> to hold text """
    classes = [ "ltk-text" ]

    def __init__(self, *args, style=DEFAULT_CSS):
        Widget.__init__(self, *args, style)


class Input(Widget):
    """ Wraps an HTML element of type <input> """
    classes = [ "ltk-input" ]
    tag = "input"

    def __init__(self, value, style=DEFAULT_CSS):
        Widget.__init__(self, style)
        self.element.val(value)


class Checkbox(Widget):
    """ Wraps an HTML element of type <input type="checkbox"> """
    classes = [ "ltk-checkbox" ]
    tag = "input"

    def __init__(self, checked, style=DEFAULT_CSS):
        Widget.__init__(self, style)
        self.element.prop("type", "checkbox")
        self.check(checked)

    def check(self, checked):
        self.element.prop("checked", "checked" if checked else None)

    def checked(self):
        return self.element.prop("checked") == "checked"


class Span(Widget):
    """ Wraps an HTML element of type <span> """
    classes = [ "ltk-span" ]
    tag = "span"


class Switch(HBox):
    """ A checkbox with special styling to resemble a switch/toggle """
    classes = [ "ltk-switch-container ltk-hbox" ]

    def __init__(self, label, checked, style=DEFAULT_CSS):
        """
        Create a new switch

        Args:
            label:str: The label for the switch
            checked:bool Whether the switch is checked or not
        """
        def toggle_edit(event):
            checked = self.element.find(".ltk-checkbox").prop("checked")
            self.element.prop("checked", checked)
        id = f"edit-switch-{get_time()}"
        HBox.__init__(self, 
            Div(label).addClass("ltk-switch-label"),
            Checkbox(True).attr("id", id).addClass("ltk-switch-checkbox").on("change", toggle_edit),
            Label("").attr("value", "edit:").attr("for", id).addClass("ltk-switch"),
        )

        self.check(checked)

    def check(self, checked):
        self.element.find(".ltk-checkbox").prop("checked", "checked" if checked else None)

    def checked(self):
        return self.element.find(".ltk-checkbox").prop("checked") == "checked"

class Label(Widget):
    """ Wraps an HTML element of type <label> browser DOM element """
    classes = [ "ltk-label" ]
    tag = "label"

    def __init__(self, label, input=None, style=DEFAULT_CSS):
        Widget.__init__(self, style)
        if input:
            self.element.append(input)
        self.element.append(label)


class Button(Widget):
    """ Wraps an HTML element of type <button> element """
    classes = [ "ltk-button" ]
    tag = "button"

    def __init__(self, label:str, click, style=DEFAULT_CSS):
        """
        Initializes a new Button instance.

        Args:
            label:str: The label for the button
            click:function(event): The event handler for this button
            style:dict [optional] CSS values to set on the element
        """
        Widget.__init__(self, style)
        self.element.text(label).on("click", proxy(click))


class Link(Text):
    """ Wraps an HTML element of type <a> """
    classes = [ "ltk-a" ]
    tag = "a" 

    def __init__(self, href, *items):
        Widget.__init__(self, *items)
        self.attr("href", href)


class Strong(Text):
    """ Wraps an HTML element of type <strong> """
    classes = [ "ltk-strong" ]
    tag = "strong"


class Important(Text):
    """ Wraps an HTML element of type <b> """
    classes = [ "ltk-b" ]
    tag = "b"


class Italic(Text):
    """ Wraps an HTML element of type <i> """
    classes = [ "ltk-i" ]
    tag = "i" 


class Paragraph(Text):
    """ Wraps an HTML element of type <p> """
    classes = [ "ltk-p" ]
    tag = "p"


class Break(Text):
    """ Wraps an HTML element of type <br> """
    classes = [ "ltk-br" ]
    tag = "br"


class Heading1(Text):
    """ Wraps an HTML element of type <h1> """
    classes = [ "ltk-h1" ]
    tag = "h1"


class Heading2(Text):
    """ Wraps an HTML element of type <h2> """
    classes = [ "ltk-h2" ]
    tag = "h2"


class Heading3(Text):
    """ Wraps an HTML element of type <h3> """
    classes = [ "ltk-h3" ]
    tag = "h3"


class Heading4(Text):
    """ Wraps an HTML element of type <h4> """
    classes = [ "ltk-h4" ]
    tag = "h4"


class OrderedList(Container):
    """ Wraps an HTML element of type <ol> """
    classes = [ "ltk-ol" ]
    tag = "ol"


class UnorderedList(Container):
    """ Wraps an HTML element of type <ul> """
    classes = [ "ltk-ul" ]
    tag = "ul"


class ListItem(Container):
    """ Wraps an HTML element of type <li> """
    classes = [ "ltk-li" ]
    tag = "li"


class Tabs(Widget):
    """ Wraps an HTML element of type jQueryUI tabs """
    classes = [ "ltk-tabs" ]
    tag = "div"
    count = 0

    def __init__(self, *tabs):
        self.name = f"ltk-tabs-{Tabs.count}"
        Tabs.count += 1
        self.labels = UnorderedList()
        Widget.__init__(self, self.labels)
        self.attr("id", self.name)
        for tab in self._flatten(tabs):
            self.add_tab(tab)
        self._handle_css(tabs)
        self.tabs()

    def add_tab(self, tab):
        tab_id = f"{self.name}-{self.labels.children().length}"
        self.labels.append(
            ListItem().append(Link(f"#{tab_id}").text(tab.attr("name")))
        )
        self.append(Div(tab).attr("id", tab_id))

    def active(self):
        return self.element.tabs("option", "active")

    def activate(self, index):
        self.element.tabs("option", "active", index)

    def get_tab(self, index):
        return self.element.find(f"li:nth-child({index + 1})")

    def get_panel(self, index):
        return self.element.children().eq(index + 1)


class File(Widget):
    """ Wraps an HTML element of type <input type=file> """
    classes = [ "ltk-file" ]
    tag = "input"

    def __init__(self, style=DEFAULT_CSS):
        Widget.__init__(self, style)
        self.element.attr("type", "file")


class DatePicker(Widget):
    """ Wraps an HTML element of type <input type=date> """
    classes = [ "ltk-datepicker" ]
    tag = "input"

    def __init__(self, style=DEFAULT_CSS):
        Widget.__init__(self, style)
        self.element.attr("type", "date")


class ColorPicker(Widget):
    """ Wraps an HTML element of type <input type=color> """
    classes = [ "ltk-colorpicker" ]
    tag = "input"

    def __init__(self, style=DEFAULT_CSS):
        Widget.__init__(self, style)
        self.element.attr("type", "color")


class RadioGroup(VBox):
    """ Wraps an HTML element of type collection of Radio buttons """
    classes = [ "ltk-vbox ltk-radiogroup" ]

    def __init__(self, *buttons, style=DEFAULT_CSS):
        name = f"ltk-radiogroup-{window.get_time()}"
        for button in buttons:
            button.find("input").attr("name", name)
        VBox.__init__(self, *buttons, style)


class RadioButton(Widget):
    """ Wraps an HTML element of type <input type="radio"> """
    classes = [ "ltk-radiobutton" ]
    tag = "input"

    def __init__(self, checked, style=DEFAULT_CSS):
        Widget.__init__(self, style)
        self.element.prop("type", "radio")
        self.element.attr("checked", "checked" if checked else None)


class Table(Widget):
    """ Wraps an HTML element of type <table> """
    classes = [ "ltk-table" ]
    tag = "table"

    def __init__(self, *rows):
        self.element = (
            window.table()
                .addClass(" ".join(self.classes))
                .append(*self._flatten(rows))
        )

    def title(self, column, title):
        window.tableTitle(self.element, column, title)

    def get(self, column, row):
        return window.tableGet(self.element, column, row)

    def set(self, column, row, value):
        window.tableSet(self.element, column, row, value)


class TableRow(Widget):
    """ Wraps an HTML element of type <tr> """
    classes = [ "ltk-tr" ]
    tag = "tr"


class TableHeader(Text):
    """ Wraps an HTML element of type <th> """
    classes = [ "ltk-th" ]
    tag = "th"


class TableData(Text):
    """ Wraps an HTML element of type <td> """
    classes = [ "ltk-td" ]
    tag = "td"


class VerticalSplitPane(Widget):
    """ Lays out its child widgets horizontally with a resize handle in the center """
    classes = [ "ltk-vertical-split-pane", "ltk-table" ]
    tag = "table"

    def __init__(self, left, right):
        """
        Places <code>left</code> and <code>right</code> next to each other.
        """
        self.element = (
            window.table()
                .addClass(" ".join(self.classes))
                .append(
                    TableRow(
                        TableData(left.resizable(to_js({"handles": "e"}))).css("padding", 0), 
                        TableData(right).css("padding", 0)
                    ).element
                )
        )
        self.width("100%")


class TextArea(Text):
    """ Wraps an HTML element of type <textarea> """
    classes = [ "ltk-td" ]
    classes = [ "ltk-textarea" ]
    tag = "textarea"

    def __init__(self, text="", style=DEFAULT_CSS):
        Widget.__init__(self, style)
        self.element.text(text)


class Code(Widget):
    """ Wraps an HTML element of type block of code """
    classes = [ "ltk-code" ]
    tag = "code"
    highlighted = False

    def __init__(self, language, code, style=DEFAULT_CSS):
        Widget.__init__(self, style)
        if not hasattr(window, "hljs"):
            inject_css("https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css")
            inject_script("https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js")
            inject_script(f"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/{language}.min.js")
        self.element.text(code).css("opacity", 0)
        schedule(self.highlight, f"{self}.highlight")

    def highlight(self):
        if self.highlighted:
            return
        if hasattr(window, "hljs"):
            window.hljs.highlightElement(self.element[0])
            self.element.animate(to_js({ "opacity": 1}))
            self.highlighted = True
        else:
            schedule(self.highlight, f"{self}.highlight", 0.1)


class Image(Widget):
    """ Wraps an HTML element of type <img> """
    classes = [ "ltk-image" ]
    tag = "img"

    def __init__(self, src, onerror=None, style=DEFAULT_CSS):
        Widget.__init__(self, style)
        self.element.referrerPolicy = "referrer"
        self.element.attr("src", src)
        if onerror:
            self.element.attr("onerror", f'this.src = "{onerror}"')


class MenuBar(HBox):
    """ Creates a horizontal menubar """
    classes = ["ltk-menubar"]


class MenuLabel(Widget):
    """ Creates a label used in menus """
    classes = ["ltk-menulabel"]

    def __init__(self, label, style=DEFAULT_CSS):
        Widget.__init__(self, style)
        self.element.text(label)


class Menu(Widget):
    """ Creates a menu """
    classes = ["ltk-menu"]

    def __init__(self, label, *items, style=DEFAULT_CSS):
        self.label = MenuLabel(label)
        self.popup = MenuPopup(*items)
        Widget.__init__(self, self.label, self.popup, style)
        self.label.on("click", proxy(lambda event: self.show(event)))
        self.on("mouseenter", proxy(lambda event: self.replace_other(event)))

    def replace_other(self, event):
        if find(".ltk-menupopup-open").length:
            _close_all_menus()
            self.show(event)

    def show(self, event):
        """ Render the menu visible """
        _close_all_menus()
        self.popup.show(self.element)
        event.preventDefault()
        return self


class Popup(Widget):
    """ Wraps an HTML element of type div that is positioned on top of all other widgets """
    classes = [ "popup" ]


class MenuPopup(Popup):
    """ Creates a menu that is a popup """
    classes = [ "ltk-menupopup" ]

    def show(self, element):
        _close_all_menus()
        find("#main").css("opacity", 0.3)
        (self
            .appendTo(jQuery(window.document.body))
            .css("top", element.offset().top + 28)
            .css("left", min(element.offset().left + 2, jQuery(window.document.body).width() - self.width() - 12))
            .addClass("ltk-menupopup-open")
        )


class MenuItem(Widget):
    """ Creates a menuitem used inside a menu """
    classes = [ "ltk-menuitem" ]

    def __init__(self, icon, label, shortcut, selected, style=DEFAULT_CSS):
        Widget.__init__(self,
            Text(icon).addClass("ltk-menuitem-icon"),
            Text(label).addClass("ltk-menuitem-label"),
            Text(shortcut).addClass("ltk-menuitem-shortcut"),
            style
        )
        self.on("click", proxy(lambda event: self.select(event)))
        self.on("select", proxy(lambda event: self.select(event)))
        if shortcut in BROWSER_SHORTCUTS:
            raise ValueError(f"Cannot capture shortcut {shortcut} as the browser won't allow that")
        if shortcut:
            shortcuts[shortcut] = self
        self.label = label
        self.selected = selected

    def select(self, event):
        _close_all_menus()
        print("select", self, self.selected)
        self.selected(self)
        event.preventDefault()


class Select(Widget):
    """ Wraps an HTML element of type <select> """
    classes = [ "ltk-select" ]
    tag = "select"

    def __init__(self, options, selected, handler, style=DEFAULT_CSS):
        Widget.__init__(self, 
            [
                Option(text).prop("selected", "selected" if text == selected else "")
                for text in options
            ],
            style
        )
        self.handler = handler
        self.element.on("change", proxy(lambda event: schedule(self.changed, f"{self}.changed")))

    def get_selected_index(self):
        return self.element.prop("selectedIndex")

    def changed(self):
        option = self.element.find("option").eq(self.get_selected_index())
        self.handler(self.get_selected_index(), option)


class Option(Text):
    """ Wraps an HTML element of type <option> """
    classes = [ "ltk-option" ]
    tag = "option"


def _close_all_menus(event=None):
    if event and jQuery(event.target).hasClass("ltk-menulabel"):
        return
    find(".ltk-menupopup-open").removeClass("ltk-menupopup-open")

jQuery(window.document.body).on("click", proxy(_close_all_menus))

def _handle_shortcuts():
    def handle_keydown(event):
        shortcut = f"{'Cmd+' if event.metaKey else ''}{event.key.upper() if event.key else ''}"
        if shortcut in shortcuts:
            event.preventDefault()
            shortcuts[shortcut].select(event)
    jQuery(window.document).on("keydown", proxy(handle_keydown))


_handle_shortcuts()