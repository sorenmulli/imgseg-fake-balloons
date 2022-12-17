# Synthetic Semantic Segmentation Training Data using WebGL
Course project for 02561 Computer Graphics at the Technical University of Denmark.

## Reproduction
### Setup
Run `make` to install the Python software.
Open `webgl-site/index.html` in any modern browser to see the examples.

### Get Fake Balloons data
You can build the synthetic dataset yourself; see `make data`.
The version used in this project is downloadable from Google Drive [here](https://drive.google.com/file/d/1k6ikalUtzpYARzGTrxpVCvUwmP9_EJ9W/view?usp=sharing) and [here](https://drive.google.com/file/d/1psLKuoBt9Ai_bP9zxUFJ_OeGAyxa1jm-/view?usp=sharing) or by running `wget` commands from the script `dev/download.sh`.

### Get COCO data
Download 2017 test and val images and annotations from [COCO download page](https://cocodataset.org/#download).
Place in a directory, e.g. `cocodata` where structure should be
```
cocodata/
├─ instances_train2017.json
├─ instances_val2017.json
├─ val2017/
│  ├─ 000000000139.jpg
│  ├─ ...
├─ train2017/
│  ├─ 000000000009.jpg
│  ├─ ...
```
### Run experiments
See `python imgseg02561/train.py --help`. 
My configuration is run when running `make train` but some paths should be configured to your data location
