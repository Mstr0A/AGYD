# AGYD (Actually Good Youtube Downloader)

A simple GUI application to download videos and audio from YouTube without ads or hassle.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Mstr0A/AGYD.git
cd AGYD
```

2. Install dependencies:
```bash
# Using pip
pip install -r requirements.txt

# Or using uv (optional)
uv sync
```

## Usage

Run the application:
```bash
# Using python
python main.py

# Using uv
uv run main.py 
```

Then simply:
1. Paste a YouTube URL
2. Choose video or audio download
3. Click download

## Building Executable (Optional)
PyInstaller is included in the requirements to create a standalone executable:
```bash

# Using python
python -m pytinstaller --onefile --noconsole main.py

# Using uv (optional)
uv run pytinstaller --onefile --noconsole main.py
```


## Requirements

- Python 3.13.7
- See `requirements.txt` for dependencies

## License

MIT License
