import unittest

from syncer.client import DirectoryClient


class ThrottleTests(unittest.TestCase):
    def test_default_limit_spaces_calls_100ms(self):
        now = [0.0]
        slept = []

        def sleep(s):
            slept.append(s)
            now[0] += s

        c = DirectoryClient("http://x", "k", clock=lambda: now[0], sleep=sleep)
        c._throttle()
        c._throttle()
        c._throttle()
        self.assertEqual(DirectoryClient.DEFAULT_MAX_RPS, 10)
        self.assertEqual(len(slept), 2)
        self.assertTrue(all(abs(s - 0.1) < 1e-9 for s in slept))


if __name__ == "__main__":
    unittest.main()
