# backtest-leverage-long-run

Attempted backtest of system similar to [Leverage for the Long Run - A Systematic Approach to Managing Risk and Magnifying Returns in Stocks](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2741701).


## Setup

* Install Python (3.10.6 was used for development) and any other programming tools. Quick links for Windows users:
  * https://www.python.org/ftp/python/3.10.7/python-3.10.7-amd64.exe
  * https://github.com/git-for-windows/git/releases/download/v2.37.3.windows.1/Git-2.37.3-64-bit.exe
  * https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user
* Do the following in the cloned repository:
  * Create virtual environment
    * `python -m venv .venv`
  * Activate environment with the command below or select interpreter in VSCode (ctrl+shift+p, Python: Select Interpreter, choose .venv)
    * `source .venv/Scripts/activate`
  * Install requirements
    * `pip install -r requirements.txt`
  * Download SPY data
    * `python python data_download.py`

Pytests should now work!
