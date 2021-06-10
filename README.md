# Stiften Alto-XML Extractor #
 
- extracting content from Alto-XML to intermediary json
- minimal preprocessing
- concatenate documents in desired time bin
- export as txt

<br>

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

<br>

## Installation

Clone repository and install requirements.

```bash
$ git clone https://github.com/centre-for-humanities-computing/xml-stiften
$ pip install -r requirements.txt
```

<br>

## Usage
There are two ways to run this script - via notebook, or CLI. You can choose whichever suits you best.
Method A is to run the scripts from a jupyter notebook (extract_stiften.ipynb).
Method B is running the extractor using a shell script (extract_stiften.sh).  

#### Run from a jupyter notebook
Open the jupyter notebook (`extract_stiften.ipynb`).  
Edit input parameters (documented inside the notebook).  
Run the chunks you need.


#### Run from command line
Open shell script (`extract_stiften.sh`)  
Edit your input parameters. 
Run with `sh extract_stiften.sh`.

<br>

## Acknowledgments
Stopwords for old Danish by [VictorHarbo](https://github.com/VictorHarbo/holberg_kaffe_tei/blob/master/stopord.txt)