import unittest
from unittest.mock import patch
from jaralidar import L_Loop, R_Loop, F_Loop

class TestLidarFunctions(unittest.TestCase):

    @patch('jaralidar.L_read_lidar')
    def test_L_Loop(self, mock_L_read_lidar):
        # Mock the LIDAR readings
        mock_L_read_lidar.side_effect = [100, 200, None, 300, 400, 500, 600, 700, 800, 900]
        
        # Test the L_Loop function
        result = L_Loop()
        self.assertEqual(result, 100)

    @patch('jaralidar.R_read_lidar')
    def test_R_Loop(self, mock_R_read_lidar):
        # Mock the LIDAR readings
        mock_R_read_lidar.side_effect = [150, 250, None, 350, 450, 550, 650, 750, 850, 950]
        
        # Test the R_Loop function
        result = R_Loop()
        self.assertEqual(result, 150)

    @patch('jaralidar.F_read_lidar')
    def test_F_Loop(self, mock_F_read_lidar):
        # Mock the LIDAR readings
        mock_F_read_lidar.side_effect = [200, 300, None, 400, 500, 600, 700, 800, 900, 1000]
        
        # Test the F_Loop function
        result = F_Loop()
        self.assertEqual(result, 200)

if __name__ == '__main__':
    unittest.main()