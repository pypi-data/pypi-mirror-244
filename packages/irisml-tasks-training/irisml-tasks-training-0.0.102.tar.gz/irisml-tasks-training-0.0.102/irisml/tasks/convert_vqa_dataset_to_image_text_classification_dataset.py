import dataclasses
import logging
import typing
import torch
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Convert VQA dataset to image text classification dataset.

    This task consideres VQA question as text input and answer as class label.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        dataset: torch.utils.data.Dataset

    @dataclasses.dataclass
    class Outputs:
        dataset: torch.utils.data.Dataset
        num_classes: int
        class_names: typing.List[str]

    def execute(self, inputs):
        class_names = self._get_class_names(inputs.dataset)
        dataset = Dataset(inputs.dataset, class_names)
        logger.info(f"Converted dataset. num_classes={len(class_names)} class_names={class_names}")
        return self.Outputs(dataset=dataset, num_classes=len(class_names), class_names=class_names)

    def dry_run(self, inputs):
        return self.execute(inputs)

    def _get_class_names(self, dataset):
        answer_set = set()
        if hasattr(dataset, 'get_targets'):
            for i in range(len(dataset)):
                answer_set.add(dataset.get_targets(i))
        else:
            for _, answer in dataset:
                answer_set.add(answer)

        return sorted(list(answer_set))


class Dataset(torch.utils.data.Dataset):
    def __init__(self, dataset, class_names):
        self._class_names = class_names
        self._class_name_to_index = {class_name: i for i, class_name in enumerate(class_names)}
        self._dataset = dataset

    def __len__(self):
        return len(self._dataset)

    def __getitem__(self, index):
        (question, image), targets = self._dataset[index]
        assert isinstance(targets, str)
        assert targets in self._class_name_to_index
        class_id = torch.tensor(self._class_name_to_index[targets], dtype=torch.long)
        return (image, question), class_id

    def get_targets(self, index):
        if hasattr(self._dataset, 'get_targets'):
            targets = self._dataset.get_targets(index)
        else:
            _, targets = self._dataset[index]

        class_id = torch.tensor(self._class_name_to_index[targets], dtype=torch.long)
        return class_id
