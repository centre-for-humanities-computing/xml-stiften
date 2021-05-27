# Stiften Alto-XML Extractor #

Description


## Prerequisites

For running in virtual environment (recommended) and assuming python is installed.

#### Windows
```bash
> pip install virtualenv
> virtualenv stiftenv
> stiftenv\Scripts\activate
```
#### Linux
```bash
$ pip install virtualenv
$ virtualenv stiftenv
$ source stiftenv/bin/activate
```


## Installation

Clone repository and install requirements.

```bash
$ git clone https://github.com/centre-for-humanities-computing/newsFluxus.git
$ pip install -r requirements.txt
```


## Usage
There are two methods, you can choose whichever suits you best.
Method A is to run the scripts from a jupyter notebook (extract_stiften.ipynb).
Method B is running the extractor using a shell script (extract_stiften.sh).  

### Method A
Open the jupyter notebook, edit input parameters (documented inside the notebook), run the chunks you need.


### Method B
Edit your input parameters in `extract_stiften.sh` and run:
```
sh extract_stiften.sh
```