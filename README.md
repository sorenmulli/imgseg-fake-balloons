
## Reproduction
### Get COCO data
Download 2017 test and val from [COCO download page](https://cocodataset.org/#download).
Place in a directory, default is `cocodata` in working directory.
Structure should be
```
cocodata/
├─ instances_train2017.json
├─ instances_val2017.json
├─ val2017/
│  ├─ 000000000139.jpg
│  ├─ ...
├─ train2017/
│  ├─ 000000000???.jpg
│  ├─ ...
```
### Run experiment
See/run commands by running `make`, then `make data`, then `make train`
