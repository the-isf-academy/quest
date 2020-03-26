# test_feature.py
# By: Jaccob Wolf
#
# file to test the implementation of a feature by running all the example games
# in the example repo.
#
# Built from pvcraven's Python Arcade example: https://github.com/pvcraven/arcade/blob/master/tests/test_examples/run_all_examples.py
# =============================================================================
# ☕️ More-Than-You-Need-To-Know Lounge ☕️
# =============================================================================
# Welcome to the More-Than-You-Need-To-Know Lounge, a chill place for code that
# you don't need to understand.

# Thanks for stopping by, we hope you find something that catches your eye.
# But don't worry if this stuff doesn't make sense yet -- as long as we know
# how to use code, we don't have to understand everything about it.

# Of course, if you really like this place, stay a while. You can ask a
# teacher about it if you're interested.
#
# =============================================================================

import unittest
import sys, io

import subprocess
import os
import glob
from xvfbwrapper import Xvfb


EXAMPLE_SUBDIR = "quest/examples/"


def _get_short_name(fullpath):
    return os.path.splitext(os.path.basename(fullpath))[0]


def _get_examples(start_path):
    query_path = os.path.join(start_path, "*.py")
    examples = glob.glob(query_path)
    examples = [_get_short_name(e) for e in examples]
    examples = [e for e in examples if e != "run_all_examples"]
    examples = [e for e in examples if not e.startswith('_')]
    examples = ["quest.examples." + e for e in examples if not e.startswith('_')]
    return examples

class TestExampleGames(unittest.TestCase):

    def setUp(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        os.environ['ARCADE_TEST'] = "TRUE"
        self.indices_in_range = None
        self.index_skip_list = None
        self.examples = _get_examples(EXAMPLE_SUBDIR)


    def test_examples(self):
        """Run all examples in the arcade/examples directory


        """
        print("Found {} examples in {}".format(len(self.examples), EXAMPLE_SUBDIR))
        for (idx, example) in enumerate(self.examples):
            with self.subTest(i=example):
                    if self.indices_in_range is not None and idx not in self.indices_in_range:
                        continue
                    if self.index_skip_list is not None and idx in self.index_skip_list:
                        continue
                    print(f"=================== Example {idx + 1:3} of {len(self.examples)}: {example}")
                    # print('%s %s (index #%d of %d)' % ('=' * 20, example, idx, len(examples) - 1))
                    cmd = 'python -m ' + example
                    errors = ""
                    completed_run = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    self.longMessage = False
                    self.assertEqual(completed_run.returncode, 0, "Error while running {}\n{}".format(example, completed_run.stderr))


if __name__ == '__main__':
    unittest.main()
