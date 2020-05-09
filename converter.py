import json, os

class ShoeSize:
    def __init__(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        f = open(os.path.join(__location__, 'shoe_size_chart.json'))
        self.chart = json.load(f);

    def convert(self, category, unit, size, outputUnits = None):
        output = {}
        if outputUnits:
            units = outputUnits
        else:
            units = list(self.chart[category].keys())
            units.remove(unit)
        for single_unit in units:
            output[single_unit] = self.chart[category][single_unit][size]
        return output

    def get_categories(self):
        return list(self.chart.keys())

    def get_measures(self):
        return list(self.chart[list(self.chart.keys())[0]].keys())

    def get_values(self, category, measure):
        if category == None or measure == None:
            return []
        else:
            return self.chart[category][measure];
