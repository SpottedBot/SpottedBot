from django.test import TestCase
from main.templatetags.stat_crunch import stat_order
# Create your tests here.


class TestStatCrunch(TestCase):
    def test_stat_order(self):
        self.assertEqual(stat_order(0), '1')
        self.assertEqual(stat_order(-1), '1')
        self.assertEqual(stat_order(''), '1')
        self.assertEqual(stat_order(93), '93')
        self.assertEqual(stat_order(590), '590')
        self.assertEqual(stat_order(1000), '1K')
        self.assertEqual(stat_order(1200), '1.2K')
        self.assertEqual(stat_order(1220), '1.2K')
        self.assertEqual(stat_order(1299), '1.3K')
        self.assertEqual(stat_order(5000), '5K')
        self.assertEqual(stat_order(554321), '554.3K')
        self.assertEqual(stat_order(5200000), '5.2M')
        self.assertEqual(stat_order(5200000000), '5.2G')
        with self.assertRaises(KeyError):
            stat_order(5200000000000)
