from core.property_finder import *


class PropertyFinderTests(unittest.TestCase, MainPageObject, SearchResultsPageObject):

    def setUp(self):
        PropertyFinder.__init__(self)
        self.driver.get('http://propertyfinder.ae')

    def test_find_property(self):
        self.search_properties()
        self.sort_properties()
        bed_count = self.select_last_property()
        self.assertEqual(int(bed_count), 2)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
