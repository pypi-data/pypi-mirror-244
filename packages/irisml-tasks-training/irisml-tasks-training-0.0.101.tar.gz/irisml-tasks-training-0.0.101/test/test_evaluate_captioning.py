import unittest
from irisml.tasks.evaluate_captioning import Task


class TestEvaluateCaptioning(unittest.TestCase):
    def test_perfect(self):
        predictions = ['Hello World Good bye', 'This is perfect test']
        ground_truths = [['Hello World good Bye'], ['This is perfect test', 'This is perfect test']]
        outputs = Task(Task.Config()).execute(Task.Inputs(predictions, ground_truths))
        self.assertAlmostEqual(outputs.bleu1, 1.0)
        self.assertAlmostEqual(outputs.bleu2, 1.0)
        self.assertAlmostEqual(outputs.bleu3, 1.0)
        self.assertAlmostEqual(outputs.bleu4, 1.0)
        self.assertAlmostEqual(outputs.cider, 10.0)

    def test_totally_wrong(self):
        predictions = ['How are you today', 'Only wrong words here']
        ground_truths = [['Hello World good Bye'], ['This is perfect test', 'This is perfect test']]
        outputs = Task(Task.Config()).execute(Task.Inputs(predictions, ground_truths))
        self.assertAlmostEqual(outputs.bleu1, 0.0)
        self.assertAlmostEqual(outputs.bleu2, 0.0)
        self.assertAlmostEqual(outputs.bleu3, 0.0)
        self.assertAlmostEqual(outputs.bleu4, 0.0)
        self.assertAlmostEqual(outputs.cider, 0.0)
