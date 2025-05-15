# My Closet
### Requirements
For this project you'll need:
- Python 3.11 or earlier (mine is 3.11)
- Qt Designer

### Installation
If you have 3.12 version or higher, Qt Designer will not work for you.
You have to create a virtual environment that will run earlier python.
1. Download Python 3.11 here: https://www.python.org/downloads/release/python-3110/
   Make sure to check “Add Python 3.11 to PATH”
2. Navigate to your projects path
3. Create the virtual environment with Python 3.11
```bash
python3.11 -m venv venv
```
4. Activate the environment (use it every time you want to start working in this project)
```bash
venv\Scripts\activate # for Windows
source venv/bin/activate # for Linux
```
5. Upgrade pip
```bash
pip install --upgrade pip setuptools wheel
```
6. Download Qt Designer
```bash
pip install pyqt5 pyqt5-tools
```
7. Deactivate the environment (use it every time you are finished working with this project)
```bash
deactivate
```
8. Open Qt Designer
```bash
pyqt5-tools designer
```

