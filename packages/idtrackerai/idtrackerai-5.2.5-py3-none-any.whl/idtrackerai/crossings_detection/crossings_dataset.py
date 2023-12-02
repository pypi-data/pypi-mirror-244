import logging
import platform
from pathlib import Path
from typing import Literal

import numpy as np
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets.folder import VisionDataset

from idtrackerai import Blob
from idtrackerai.network import DataLoaderWithLabels
from idtrackerai.tracker.identity_dataset import duplicate_PCA_images
from idtrackerai.utils import conf, load_id_images, track


class CrossingDataset(VisionDataset):
    images: np.ndarray
    labels: np.ndarray

    def __init__(
        self,
        blobs_list: list[Blob] | dict[str, list[Blob]],
        id_images_file_paths: list[Path],
        scope,
        transform=None,
    ):
        super().__init__("", transform=transform)
        self.id_images_file_paths = id_images_file_paths
        self.blobs = blobs_list
        self.scope = scope
        self.get_data()

    def get_data(self):
        if isinstance(self.blobs, dict):
            logging.info(f"Generating crossing {self.scope} set.")
            crossings_images = self.get_images_indices(image_type="crossings")
            crossing_labels = np.ones(len(crossings_images), np.int64)
            # some machines do int=np.int32 but CrossEntropyLoss expects int64

            logging.info(f"Generating single individual {self.scope} set")
            individual_images = self.get_images_indices(image_type="individuals")
            individual_labels = np.zeros(len(individual_images), np.int64)

            logging.info("Preparing images and labels")
            images_indices = crossings_images + individual_images
            self.images = load_id_images(self.id_images_file_paths, images_indices)
            self.images = np.expand_dims(self.images, axis=-1)

            self.labels = np.concatenate([crossing_labels, individual_labels], axis=0)

            if self.scope == "training":
                self.images, self.labels = duplicate_PCA_images(
                    self.images, self.labels
                )

        elif isinstance(self.blobs, list):
            images_indices = self.get_images_indices()
            self.images = load_id_images(self.id_images_file_paths, images_indices)
            self.images = np.expand_dims(self.images, axis=-1)
            self.labels = np.zeros(len(self.images))

    def get_images_indices(self, image_type: str = "") -> list[tuple[int, int]]:
        if image_type:
            assert isinstance(self.blobs, dict)
            blobs = self.blobs[image_type]
        else:
            assert isinstance(self.blobs, list)
            blobs = self.blobs

        return [(blob.id_image_index, blob.episode) for blob in blobs]

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        image = self.images[index]
        target = self.labels[index]
        if self.transform is not None:
            image = self.transform(image)
        return image, target


def get_train_validation_and_eval_blobs(
    blobs_in_video: list[list[Blob]],
    number_of_animals: int,
    ratio_validation: float = 0.1,
) -> tuple[dict[str, list[Blob]], dict[str, list[Blob]], list[Blob]]:
    """Given a list of blobs return 2 dictionaries (training_blobs, validation_blobs),
    and a list (toassign_blobs).

    :param list_of_blobs:
    :param ratio_validation:
    :return: training_blobs, validation_blobs, toassign_blobs
    """
    logging.info("Get list of blobs for training, validation and eval")

    individuals = []
    crossings = []
    toassign_blobs = []
    for blobs_in_frame in track(blobs_in_video, "First individual/crossing assignment"):
        in_a_global_fragment_core = len(blobs_in_frame) == number_of_animals
        for blob in blobs_in_frame:
            if in_a_global_fragment_core or blob.is_a_sure_individual():
                blob.used_for_training_crossings = True
                blob.is_an_individual = True
                individuals.append(blob)
            elif blob.is_a_sure_crossing():
                blob.used_for_training_crossings = True
                blob.is_an_individual = False
                crossings.append(blob)
            else:
                blob.used_for_training_crossings = False
                toassign_blobs.append(blob)

    # clear no longer useful cached properties
    for blobs_in_frame in blobs_in_video:
        for blob in blobs_in_frame:
            blob.__dict__.pop("has_a_next_crossing", None)
            blob.__dict__.pop("has_a_previous_crossing", None)
            blob.__dict__.pop("has_multiple_next", None)
            blob.__dict__.pop("has_multiple_previous", None)

    logging.debug(
        f"{len(individuals)} individual, "
        f"{len(crossings)} crossing and "
        f"{len(toassign_blobs)} unknown blobs in total"
    )

    # Shuffle and make crossings and individuals even
    rng = np.random.default_rng()
    rng.shuffle(individuals)
    rng.shuffle(crossings)

    crossings = crossings[: conf.MAX_IMAGES_PER_CLASS_CROSSING_DETECTOR]
    individuals = individuals[: conf.MAX_IMAGES_PER_CLASS_CROSSING_DETECTOR]

    n_blobs_crossings = len(crossings)
    n_blobs_individuals = len(individuals)
    n_individual_blobs_validation = int(n_blobs_individuals * ratio_validation)
    n_crossing_blobs_validation = int(n_blobs_crossings * ratio_validation)

    # split training and validation
    validation_blobs = {
        "individuals": individuals[:n_individual_blobs_validation],
        "crossings": crossings[:n_crossing_blobs_validation],
    }

    training_blobs = {
        "individuals": individuals[n_individual_blobs_validation:],
        "crossings": crossings[n_crossing_blobs_validation:],
    }

    ratio_crossings = n_blobs_crossings / (n_blobs_crossings + n_blobs_individuals)
    training_blobs["weights"] = [ratio_crossings, 1 - ratio_crossings]

    logging.info(
        f"{len(training_blobs['individuals'])} individual and "
        f"{len(training_blobs['crossings'])} crossing blobs for training\n"
        f"{len(validation_blobs['individuals'])} individual and "
        f"{len(validation_blobs['crossings'])} crossing blobs for validation\n"
        f"{len(toassign_blobs)} blobs to test"
    )

    return training_blobs, validation_blobs, toassign_blobs


if platform.system() in ("Windows", "Darwin"):
    # Using multiprocessing in Windows and MacOS causes a
    # recursion limit error difficult to debug
    num_workers = 0
else:
    num_workers = 1


def get_crossing_dataloader(
    id_images_file_paths: list[Path],
    blobs: list[Blob] | dict[str, list[Blob]],
    scope: Literal["training", "validation", "test"],
) -> DataLoaderWithLabels:
    logging.info("Creating %s CrossingDataset", scope)

    dataset = CrossingDataset(
        blobs, id_images_file_paths, scope=scope, transform=transforms.ToTensor()
    )
    batch_size = (
        conf.BATCH_SIZE_DCD if scope == "training" else conf.BATCH_SIZE_PREDICTIONS_DCD
    )

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=scope == "training",
        num_workers=num_workers,
        persistent_workers=num_workers > 0,
    )
