from flask import Flask, render_template, request, send_from_directory
import os
import requests

app = Flask(__name__)
DOWNLOAD_FOLDER = '/app/downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_pdfs', methods=['POST'])
def download_pdfs():
    with open('pdf_links.txt', 'r') as file:
        pdf_urls = file.readlines()
    for link in pdf_urls:
        link = link.strip()  # Remove any leading/trailing whitespace
        if link:  # Ensure the link is not empty
            try:
                response = requests.get(link, headers=headers)
                response.raise_for_status()  # Check if the request was successful
                # Extract the PDF file name from the URL
                pdf_name = os.path.join(DOWNLOAD_FOLDER, link.split("/")[-1])
                # Save the PDF file
                with open(pdf_name, "wb") as pdf_file:
                    pdf_file.write(response.content)
                print(f"Downloaded: {pdf_name}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {link}: {e}")

    return 'All PDFs have been downloaded successfully!'

@app.route('/show_pdfs', methods=['POST'])
def show_pdfs():
    pdf_files = os.listdir(DOWNLOAD_FOLDER)
    return render_template('show_pdfs.html', pdf_files=pdf_files)

@app.route('/downloads/<filename>')
def download(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run()
