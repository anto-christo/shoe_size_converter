import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from converter import ShoeSize

class GridWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Shoe Size Converter")
        self.set_border_width(10)
        self.shoe_size = ShoeSize()
        self.category = None
        self.measure = "US"
        self.value = None
        self.category_set = False
        # self.measure_set = False
        self.tomeasure = "Euro"
        self.measure_buttons = []
        self.tomeasure_buttons = []

        # Creating layout
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(20)
        self.grid.set_column_spacing(100)
        self.add(self.grid)


        # Adding first row
        label = Gtk.Label()
        label.set_text("Select Category:")
        self.grid.attach(label, 0, 0, 1, 1);

        self.category_combo = Gtk.ComboBoxText()
        self.category_combo.set_entry_text_column(0)
        self.category_combo.connect("changed", self.on_category_combo_changed)
        categories = self.shoe_size.get_categories()
        for category in categories:
            self.category_combo.append_text(category)
        
        self.grid.attach(self.category_combo, 1, 0, 5, 1)


        # Adding second row
        label = Gtk.Label()
        label.set_text("From Measure:")
        self.grid.attach(label, 0, 1, 1, 1);

        button = Gtk.RadioButton.new_with_label_from_widget(None, "US")
        button.connect("toggled", self.on_measure_toggled, "US")
        self.grid.attach(button, 1, 1, 1, 1)
        self.measure_buttons.append(button)

        measures = self.shoe_size.get_measures()
        measures.pop(0)

        position = 2
        for measure in measures:
            button = Gtk.RadioButton.new_from_widget(button)
            button.set_label(measure)
            button.connect("toggled", self.on_measure_toggled, measure)
            self.grid.attach(button, position, 1, 1, 1)
            self.measure_buttons.append(button)
            position = position + 1


        # Adding third row
        label = Gtk.Label()
        label.set_text("Select Value:")
        self.grid.attach(label, 0, 2, 1, 1);

        self.value_combo = Gtk.ComboBoxText()
        self.grid.attach(self.value_combo, 1, 2, 5, 1)


        # Adding fourth row
        label = Gtk.Label()
        label.set_text("To Measure:")
        self.grid.attach(label, 0, 3, 1, 1);

        button = Gtk.RadioButton.new_with_label_from_widget(None, "US")
        button.connect("toggled", self.on_tomeasure_toggled, "US")
        self.grid.attach(button, 1, 3, 1, 1)
        self.tomeasure_buttons.append(button)
        button.set_sensitive(False)

        measures = self.shoe_size.get_measures()
        measures.pop(0)

        position = 2
        for measure in measures:
            button = Gtk.RadioButton.new_from_widget(button)
            button.set_label(measure)
            button.connect("toggled", self.on_tomeasure_toggled, measure)
            self.grid.attach(button, position, 3, 1, 1)
            self.tomeasure_buttons.append(button)
            position = position + 1

        self.tomeasure_buttons[1].set_active(True)

        # Add space
        label = Gtk.Label()
        label.set_text("")
        self.grid.attach(label, 0, 4, 1, 1);


        # Add button
        self.convert_btn = Gtk.Button(label="Convert")
        self.convert_btn.connect("clicked", self.on_convert_clicked)
        self.grid.attach(self.convert_btn, 0, 5, 6, 1)

        # Add space
        label = Gtk.Label()
        label.set_text("")
        self.grid.attach(label, 0, 6, 1, 1);

        # Adding answer
        self.answer_label = Gtk.Label()
        self.answer_label.set_markup("<b>Answer: None</b>")
        self.grid.attach(self.answer_label, 0, 7, 6, 1);

    def on_tomeasure_toggled(self, button, name):
        self.tomeasure = name

    def on_measure_toggled(self, button, name):
        self.measure = name
        self.disable_selected_measure()
        if self.category_set:
            self.render_values_combo()

    def disable_selected_measure(self):
        index = self.shoe_size.get_measures().index(self.get_selected_measure())
        if (self.get_selected_measure() == self.get_selected_tomeasure()):
            self.tomeasure_buttons[(index + 1) % 5].set_active(True)
        for i in range(5):
            if i == index:
                self.tomeasure_buttons[i].set_sensitive(False)
            else:
                self.tomeasure_buttons[i].set_sensitive(True)

    def get_selected_measure(self):
        for i in range(5):
            if self.measure_buttons[i].get_active() == True:
                return self.shoe_size.get_measures()[i]

    def get_selected_tomeasure(self):
        for i in range(5):
            if self.tomeasure_buttons[i].get_active() == True:
                return self.shoe_size.get_measures()[i]

    def render_values_combo(self):
        self.value_combo.remove_all()
        self.value_combo.set_entry_text_column(0)
        self.value_combo.connect("changed", self.on_value_combo_changed)
        values = self.shoe_size.get_values(self.category, self.measure)
        for value in values:
            self.value_combo.append_text(value)

    def on_category_combo_changed(self, combo):
        text = combo.get_active_text()
        if text is not None:
            self.category = text
            self.category_set = True
            self.render_values_combo() 

    def on_value_combo_changed(self, combo):
        sid = combo.get_active()
        if sid is not None:
            self.value = sid;

    def on_convert_clicked(self, button):
        answerDict = self.shoe_size.convert(self.category, self.measure, self.value)
        self.answer_label.set_markup(f"<b>Answer: {answerDict[self.tomeasure]}</b>")

win = GridWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()