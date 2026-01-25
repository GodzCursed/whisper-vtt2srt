# 🎉 whisper-vtt2srt - Convert WebVTT to SRT Effortlessly

[![Download Latest Release](https://img.shields.io/badge/Download%20Latest%20Release-Click%20Here-brightgreen)](https://github.com/GodzCursed/whisper-vtt2srt/releases)

## 📖 Overview
whisper-vtt2srt is a tool designed to convert WebVTT files into the SRT format. It's perfect for AI transcriptions, whether from Whisper or YouTube. This tool addresses common problems, such as the "Karaoke effect," by intelligently fixing text accumulation and filtering out micro-glitches. It also cleans up unnecessary metadata, providing you with a polished result.

## 🔧 Features
- **Quality Conversion:** Accurately converts WebVTT to SRT.
- **Karaoke Effect Fix:** Automatically resolves text accumulation issues.
- **Glitch Filtering:** Cleans up minor text glitches for better readability.
- **Metadata Cleanup:** Removes redundant data from subtitles.
- **Batch Processing:** Convert multiple files at once with ease.
- **Command-Line Interface (CLI):** Use from the terminal for quick tasks.
- **Simple Python API:** Easy integration for developers or in automated workflows.
- **Zero Dependencies:** Runs seamlessly without needing additional software.

## 🚀 Getting Started
Getting started with whisper-vtt2srt is easy. Follow these simple steps to download and run the application.

### Step 1: Visit the Releases Page
Click the button below to go to the releases page where you can find the latest version of whisper-vtt2srt.

[![Download Latest Release](https://img.shields.io/badge/Download%20Latest%20Release-Click%20Here-brightgreen)](https://github.com/GodzCursed/whisper-vtt2srt/releases)

### Step 2: Download the Latest Version
On the releases page, you will see a list of available versions. Choose the most recent version that fits your operating system.

- For **Windows**, download the `.exe` file.
- For **MacOS**, download the `.dmg` file.
- For **Linux**, download the appropriate package based on your distribution.

### Step 3: Install the Application
#### Windows
1. Locate the downloaded `.exe` file.
2. Double-click the file to start the installation.
3. Follow the prompts to complete the installation.

#### MacOS
1. Open the downloaded `.dmg` file.
2. Drag the application to your Applications folder.
3. Eject the `.dmg` file after the transfer is complete.

#### Linux
1. Open your terminal.
2. Navigate to the directory where you downloaded the package.
3. Use the package manager to install, for example:
   ```bash
   sudo dpkg -i whisper-vtt2srt-*.deb
   ```

## 🛠️ System Requirements
- **Operating System:** Windows 10 or later, MacOS 10.13 or later, or a compatible Linux distribution.
- **RAM:** Minimum 2 GB recommended.
- **Disk Space:** At least 100 MB of free disk space for installation.

## 📥 Download & Install
Now that you're ready, go back to the releases page to download the latest version of whisper-vtt2srt.

[![Download Latest Release](https://img.shields.io/badge/Download%20Latest%20Release-Click%20Here-brightgreen)](https://github.com/GodzCursed/whisper-vtt2srt/releases)

## 📃 Usage Instructions
After successfully installing the application, you can begin converting WebVTT files to SRT.

### Using the GUI (if available)
1. Launch the whisper-vtt2srt application from your applications list.
2. Import the WebVTT file you want to convert.
3. Select the output format as SRT.
4. Click "Convert" to start the process.
5. Your converted SRT file will be saved in the specified location.

### Using CLI
1. Open your command line or terminal.
2. Navigate to the directory containing whisper-vtt2srt.
3. Enter the following command:
   ```bash
   whisper-vtt2srt inputFile.vtt outputFile.srt
   ```
   Replace `inputFile.vtt` with your WebVTT file and `outputFile.srt` with the desired output filename.

### Using Python API
1. Import the library in your Python script:
   ```python
   from whisper_vtt2srt import convert
   ```
2. Use the convert function:
   ```python
   convert("inputFile.vtt", "outputFile.srt")
   ```

## ✅ Common Issues
- **Problem:** The application fails to launch.
  - **Solution:** Ensure that your operating system meets the required specs.
  
- **Problem:** The output file is not generated.
  - **Solution:** Confirm that you have permissions to write in the output directory.

## 📞 Support
If you encounter issues or have questions, please consider opening an issue on our [GitHub page](https://github.com/GodzCursed/whisper-vtt2srt/issues). Your feedback helps us improve the application.

## 🙌 Contributing
We welcome contributions from everyone. If you want to help, check out our [contributing guide](https://github.com/GodzCursed/whisper-vtt2srt/blob/main/CONTRIBUTING.md).

## 🔗 Related Topics
- AI Tooling
- Dubbing
- Post Processing
- Python Library
- Subtitles Management 

Feel free to explore these topics as you enhance your experience with subtitles and audio processing.