import unittest

movements_map = {
    'RR': {'distance': 10, 'rotation': 100, 'upDir': 14, 'isEmpty': True, 'player': None, 'row': 0, 'col': 0},
    'GR': {'distance': 10, 'rotation': 100, 'upDir': 10, 'isEmpty': True, 'player': None, 'row': 1, 'col': 0},
    'BR': {'distance': 10, 'rotation': 100, 'upDir': 6, 'isEmpty': True, 'player': None, 'row': 2, 'col': 0},
    'BG': {'distance': 6, 'rotation': 100, 'upDir': 6, 'isEmpty': True, 'player': None, 'row': 2, 'col': 1},
    'RG': {'distance': 6, 'rotation': 100, 'upDir': 14, 'isEmpty': True, 'player': None, 'row': 0, 'col': 1},
    'GG': {'distance': 6, 'rotation': 100, 'upDir': 10, 'isEmpty': True, 'player': None, 'row': 1, 'col': 1},
    'GB': {'distance': 2, 'rotation': 100, 'upDir': 10, 'isEmpty': True, 'player': None, 'row': 1, 'col': 2},
    'RB': {'distance': 2, 'rotation': 100, 'upDir': 14, 'isEmpty': True, 'player': None, 'row': 0, 'col': 2},
    'BB': {'distance': 2, 'rotation': 100, 'upDir': 6, 'isEmpty': True, 'player': None, 'row': 2, 'col': 2}
}


def getBestMoveKey(best_move):
    for key, values in movements_map.items():
        if (values['row'], values['col']) == best_move:
            return key
    else:
        return None


class TestGetBestMoveKey(unittest.TestCase):

    def test_existing_key(self):
        self.assertEqual(getBestMoveKey((0, 1)), 'RG')

    def test_all_keys(self):
        for key, values in movements_map.items():
            coordinates = (values['row'], values['col'])
            actual_key = getBestMoveKey(coordinates)
            self.assertEqual(actual_key, key)

    def test_nonexistent_key(self):
        self.assertIsNone(getBestMoveKey((10, 10)))

    def test_edge_case(self):
        self.assertEqual(getBestMoveKey((2, 2)), 'BB')



if __name__ == '__main__':
    unittest.main()
