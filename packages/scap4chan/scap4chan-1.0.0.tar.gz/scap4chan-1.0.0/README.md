## Introduction

A 4chan scraper to scrap partiular board's all its contents and store into a folder. It can also scrap all the images from a particular thread.

## Requirements
1. TQDM
2. Requests
3. BASC-py4chan

## Installation
```Terminal
pip install scap4chan
```

#### Usage
```python
from scap4chan import scrape4chan_board

scrape4chan_board('pol', num_threads=10, debug=False)
```