# BarCodeScanner

BarCodeScanner is a macOS application that utilizes your MacBook's front camera to scan barcodes and QR codes.

## Features

- Scans barcodes and QR codes using your MacBook's front camera
- Automatically copies decoded content to the clipboard
- If granted macOS Privacy & Security Accessibility access, it can input content directly at the current cursor position

## Prerequisites

Before installation, ensure you have the following system dependency:
```
brew install zbar
```

## Installation

You have two options for installation:

1. Download the pre-compiled app from the [releases page](insert_link_here).

2. Compile the app yourself:

    a. Install Python dependencies:
    ```
    pip install -r requirements.txt
    ```

    b. Generate the spec file:
    ```
    pyi-makespec --name="BarCodeReader" --windowed --icon=icon.icns main.py
    ```

    c. Modify the `BarCodeReader.spec` file:
    
    Add the following at the beginning of the file:
    ```python
    import plistlib
    with open('Info.plist', 'rb') as f:
        custom_plist = plistlib.load(f)
    ```

    Add this line within the `BUNDLE()` function:
    ```python
    info_plist=custom_plist,
    ```

    d. Build the application:
    ```
    pyinstaller BarCodeReader.spec
    ```

    e. Find the compiled application in the `dist` directory.

## Usage

[Add instructions on how to use the application here]

## Contributing

[Add information about how others can contribute to the project]

## License

[Specify the license under which this project is released]
