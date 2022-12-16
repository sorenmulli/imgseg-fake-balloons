import os
from typing import Optional, Callable, Tuple, Any
from PIL import Image
import numpy as np
from torchvision.datasets import VisionDataset


class FakeBalloons(VisionDataset):
    def __init__(
        self,
        root: str,
        transform: Optional[Callable] = None,
        target_transform: Optional[Callable] = None,
        transforms: Optional[Callable] = None,
    ) -> None:
        super().__init__(root, transforms, transform, target_transform)
        self.img_ids = sorted(
            list({x.split(".")[0] for x in os.listdir(self.root) if x.endswith("png")})
        )
        assert len(self), f"Did not find image files in {self.root}"

    def _load_image(self, img_id: str) -> Image.Image:
        return Image.open(os.path.join(self.root, f"{img_id}.png")).convert("RGB")

    def _load_target(self, img_id: str):
        target_rgb = np.array(
            Image.open(os.path.join(self.root, f"{img_id}.label.png")).convert("RGB")
        )
        target = np.zeros(target_rgb.shape[:2], dtype=np.uint8)
        # These values fit with construction from `randomness.js`
        for i in range(3):
            target[target_rgb[:, :, i] == 255] = i + 1
        return Image.fromarray(target)

    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        img_id = self.img_ids[index]
        image = self._load_image(img_id)
        target = self._load_target(img_id)

        if self.transforms is not None:
            image, target = self.transforms(image, target)

        return image, target

    def __len__(self) -> int:
        return len(self.img_ids)


if __name__ == "__main__":
    dataset = FakeBalloons("dataset/v1")
    image, target = dataset[1]
    print(image, target)
    breakpoint()
