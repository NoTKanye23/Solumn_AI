import unittest

from syncer.client import DirectoryClient


class ThrottleTests(unittest.TestCase):
    def test_calls_are_spaced_at_least_one_over_max_rps_apart(self):
        now = [0.0]
        slept = []

        def sleep(s):
            slept.append(s)
            now[0] += s

        c = DirectoryClient("http://x", "k", clock=lambda: now[0], sleep=sleep)
        c._throttle()
        c._throttle()
        c._throttle()
        self.assertEqual(len(slept), 2)
        expected = 1.0 / DirectoryClient.DEFAULT_MAX_RPS
        self.assertTrue(all(abs(s - expected) < 1e-9 for s in slept))


if __name__ == "__main__":
    unittest.main()
