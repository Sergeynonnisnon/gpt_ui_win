
# 🎧 GPT UI


## 📖 Demo


## 🚀 Getting Started

Follow these steps to set up and run GPT UI on your local machine.

### 📋 Prerequisites

- Python >=3.8.0
- An OpenAI API key that can access OpenAI API (set up a paid account OpenAI account)
- Windows OS (Not tested on others)
- FFmpeg 

If FFmpeg is not installed in your system, you can follow the steps below to install it.

First, you need to install Chocolatey, a package manager for Windows. Open your PowerShell as Administrator and run the following command:
```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
Once Chocolatey is installed, you can install FFmpeg by running the following command in your PowerShell:
```
choco install ffmpeg
```
Please ensure that you run these commands in a PowerShell window with administrator privileges. If you face any issues during the installation, you can visit the official Chocolatey and FFmpeg websites for troubleshooting.

### 🔧 Installation

1. Clone the repository:

   ```
   git clone https://github.com/Sergeynonnisnon/gpt_ui_win
   ```

2. Navigate to the `gpt_ui_win` folder and install venv:

   ```
   python -m venv venv
   venv/Scripts/activate
   cd gpt_ui_win
   
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```
   
4. Create a `.env` file in the  directory and add your OpenAI API key:

   -  Open up your text editor of choice and enter the following content:
   
      ```
      OPENAI_API_KEY="API KEY"
      ```
      Replace "API KEY" with your actual OpenAI API key.

### 🎬 Running GPT UI

Run the main script:

```
python main.py  --api
```


Upon initiation, GPT UI will begin transcribing your microphone input and speaker output in real-time, generating a suggested response based on the conversation. Please note that it might take a few seconds for the system to warm up before the transcription becomes real-time.

The --api flag will use the whisper api for transcriptions. This significantly enhances transcription speed and accuracy, and it works in most languages (rather than just English without the flag). It's expected to become the default option in future releases. However, keep in mind that using the Whisper API will consume more OpenAI credits than using the local model. This increased cost is attributed to the advanced features and capabilities that the Whisper API provides. Despite the additional expense, the substantial improvements in speed and transcription accuracy may make it a worthwhile investment for your use case.

## 📖 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## FORK details

https://github.com/SevaSk/ecoute