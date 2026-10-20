import unittest
import torch
from torch_rand_range_lab.benchmarks.run import numerical_tests


class NumericalTests(unittest.TestCase):
    def test_cpu_contract(self):
        torch.set_num_threads(2)
        self.assertEqual(numerical_tests(torch.device("cpu"))["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
