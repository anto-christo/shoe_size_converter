from main import GridWindow
from converter import ShoeSize
from gi.repository import Gtk

gw = GridWindow()
shoe_size = ShoeSize()

# Component positions
def test_category_label_position():
    obj = gw.grid.get_child_at(0, 0)
    if isinstance(obj, Gtk.Label):
        assert obj.get_text() == "Select Category:"

def test_from_measure_label_position():
    obj = gw.grid.get_child_at(0, 1)
    if isinstance(obj, Gtk.Label):
        assert obj.get_text() == "From Measure:"

def test_row_spacing():
    assert gw.grid.get_row_spacing() == 10

# Initial
def test_category_not_selected():
    assert gw.category_combo.get_active() == -1

def test_from_us_selected():
    assert gw.measure_buttons[0].get_active() == True

def test_to_us_disabled():
    assert gw.tomeasure_buttons[0].get_sensitive() == False

def test_value_empty():
    assert gw.value_combo.set_active(0) == None

def test_to_us_not_selected():
    assert gw.tomeasure_buttons[0].get_active() == False

def test_answer_none():
    assert gw.answer_label.get_label() == f"<b>Answer: None</b>"

# User operations
def test_value_loaded():
    gw.category_combo.set_active(0)
    values = shoe_size.get_values("Men", "US")
    for value in values:
        gw.value_combo.set_active(0)
        print (gw.value_combo.get_active(), value)
        if gw.value_combo.get_active_text() != value:
            assert False
        else:
            gw.value_combo.remove(0)
    assert True

def test_value_changed_on_category_change():
    gw.category_combo.set_active(1)
    values = shoe_size.get_values("Women", "US")
    for value in values:
        gw.value_combo.set_active(0)
        if gw.value_combo.get_active_text() != value:
            assert False
        else:
            gw.value_combo.remove(0)
    assert True

def test_value_changed_on_measure_change():
    gw.measure_buttons[1].set_active(True)
    values = shoe_size.get_values("Women", "Euro")
    for value in values:
        gw.value_combo.set_active(0)
        if gw.value_combo.get_active_text() != value:
            assert False
        else:
            gw.value_combo.remove(0)
    assert True

def test_to_euro_disabled():
    assert gw.tomeasure_buttons[1].get_sensitive() == False

def test_to_euro_not_selected():
    assert gw.tomeasure_buttons[1].get_active() == False

# Font
def test_answer_text():
    gw.category_combo.set_active(0)
    gw.measure_buttons[0].set_active(True)
    gw.value_combo.set_active(0)
    gw.tomeasure_buttons[1].set_active(True)
    gw.convert_btn.emit("clicked")
    assert gw.answer_label.get_label() == f"<b>Answer: 35</b>"