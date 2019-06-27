from torch.utils.data import DataLoader
import torchvision.datasets as datasets
import torchvision.transforms as transforms

from sotabench.core import BenchmarkResult
from sotabench.utils import send_model_to_device

from .utils import collate_fn, evaluate_segmentation, JointCompose, DefaultPascalTransform


class PASCALVOC:

    dataset = datasets.VOCSegmentation
    normalize = transforms.Normalize(*([103.939, 116.779, 123.68], [1.0, 1.0, 1.0]))
    transforms = JointCompose([DefaultPascalTransform(target_size=(512, 512), ignore_index=255)])

    @classmethod
    def benchmark(cls, model, dataset_year='2007', input_transform=None, target_transform=None, transforms=None,
                  model_output_transform=None, device: str = 'cuda', data_root: str = './.data', num_workers: int = 4,
                  batch_size: int = 128, num_gpu: int = 1, paper_model_name: str = None, paper_arxiv_id: str = None,
                  paper_pwc_id: str = None, pytorch_hub_url: str = None) -> BenchmarkResult:

        config = locals()
        model, device = send_model_to_device(model, device=device, num_gpu=num_gpu)
        model.eval()

        if not input_transform or target_transform or transforms:
            transforms = cls.transforms

        test_dataset = cls.dataset(root=data_root, image_set='val', year=dataset_year, transform=input_transform,
                                   target_transform=target_transform, transforms=transforms, download=True)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=True,
                                 collate_fn=collate_fn)
        test_loader.no_classes = 21  # Number of classes for PASCAVoc
        test_results = evaluate_segmentation(model=model, model_output_transform=model_output_transform, test_loader=test_loader, device=device)

        print(test_results)

        return BenchmarkResult(task="Semantic Segmentation", benchmark=cls, config=config, dataset=test_dataset,
                               results=test_results, pytorch_hub_url=pytorch_hub_url, paper_model_name=paper_model_name,
                               paper_arxiv_id=paper_arxiv_id, paper_pwc_id=paper_pwc_id)