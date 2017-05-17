import unittest
from .. import spidy


class SpidyTest(unittest.TestCase):

    def test_main(self):
        self.test_url = 'http://david.com'
        with open('david.com_crawling.txt') as f:
            data = f.read()
        self.result = spidy.main(self.test_url)
        self.assertEqual(self.result, data)


if __name__ == '__main__':
    unittest.main()