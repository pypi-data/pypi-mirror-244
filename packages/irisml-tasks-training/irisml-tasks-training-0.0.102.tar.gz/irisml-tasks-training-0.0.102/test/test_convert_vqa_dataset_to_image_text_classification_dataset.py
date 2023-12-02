import unittest
import PIL.Image
import torch
from irisml.tasks.convert_vqa_dataset_to_image_text_classification_dataset import Task


class TestConvertVqaDatasetToImageTextClassificationDataset(unittest.TestCase):
    def test_simple(self):
        dataset = [(('question1', PIL.Image.new('RGB', (10, 10))), 'answer1'), (('question2', PIL.Image.new('RGB', (10, 10))), 'answer2'), (('question3', PIL.Image.new('RGB', (10, 10))), 'answer1')]

        outputs = Task(Task.Config()).execute(Task.Inputs(dataset))
        self.assertEqual(len(outputs.dataset), 3)
        self.assertEqual(outputs.num_classes, 2)
        self.assertEqual(outputs.class_names, ['answer1', 'answer2'])
        self.assertIsInstance(outputs.dataset[0][0][0], PIL.Image.Image)
        self.assertEqual(outputs.dataset[0][0][1], 'question1')
        self.assertIsInstance(outputs.dataset[0][1], torch.Tensor)

        self.assertEqual(outputs.dataset[0][1], torch.tensor(0, dtype=torch.long))
        self.assertEqual(outputs.dataset[1][1], torch.tensor(1, dtype=torch.long))
        self.assertEqual(outputs.dataset[2][1], torch.tensor(0, dtype=torch.long))
