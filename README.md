# Fresh Produce Analyzer

The Fresh Produce Analyzer is a Streamlit application that uses machine learning (Vertex AI) to assess the freshness of fruits and vegetables from images. It identifies the produce, evaluates its freshness on a scale of 1-10, predicts remaining shelf life, and lists key visual indicators. The app also maintains a history of analyses and can generate a PDF report of the results.

## Features

- **Produce Identification:** Detects the type of fruit or vegetable.
- **Freshness Assessment:** Provides a freshness score from 1-10.
- **Shelf Life Prediction:** Estimates the remaining days of freshness.
- **Visual Indicators:** Lists the visual cues that influenced the assessment.
- **Analysis History:** Tracks all analyzed items with timestamps.
- **PDF Report Generation:** Exports the analysis history to a PDF report.

## Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your-repo/fresh-produce-analyzer.git
    ```

2. **Navigate to the Project Directory:**
    ```bash
    cd fresh-produce-analyzer/Freshness
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Setup

- **Google Cloud Credentials:**
  - Obtain a Google Cloud service account key with access to Vertex AI.
  - Add the credentials to the Streamlit `secrets.toml` file in the following format:

    ```toml
    [GOOGLE_APPLICATION_CREDENTIALS]
    type = "<service_account_type>"
    project_id = "<your_project_id>"
    private_key_id = "<your_private_key_id>"
    private_key = "<your_private_key>"
    client_email = "<your_service_account_email>"
    client_id = "<your_client_id>"
    auth_uri = "https://accounts.google.com/o/oauth2/auth"
    token_uri = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
    client_x509_cert_url = "<your_cert_url>"

    [GOOGLE_CLOUD_PROJECT]
    "<your_gcp_project_id>"

    [GCP_MODEL_CRED]
    "<your_model_reference>"
    ```
    
  - Ensure that the `GCP_MODEL_CRED` in the `secrets.toml` corresponds to your Vertex AI model reference.

## Usage

1. **Run the Application:**
    ```bash
    streamlit run main.py
    ```

2. **Image Input:**
   - **Upload Image:** Select an image file (`.jpg`, `.jpeg`, `.png`) of the produce.
   - **Camera Input:** Use your device’s camera to capture an image (browser/device support required).

3. **Analyze Produce:**
   - Click **Analyze Produce** to run the analysis.

4. **View Results:**
   - The app displays the produce type, freshness score, shelf life days, and key visual indicators.

5. **History & PDF Report:**
   - All analyzed items are listed in a history table.
   - Click **Generate PDF Report** to download a comprehensive PDF summary of all analyses.

## Project Structure

- **main.py:** The main Streamlit application (UI and user interactions).
- **analysis.py:** Functions for prompt creation, image analysis, and response parsing.
- **utils.py:** Utility functions for updating session state data.
- **generate_pdf.py:** Logic for generating PDF reports.
- **requirements.txt:** Lists all required Python dependencies.

## Dependencies

- **Streamlit:** For the web application interface.
- **Vertex AI Python SDK:** To interact with Google Cloud’s Vertex AI.
- **Pillow (PIL):** For image manipulation.
- **Pandas:** For handling tabular data and displaying history.
- **ReportLab:** For generating the PDF report.
- **Google OAuth2:** For authenticating with Google Cloud services.

## Notes

- A stable internet connection is required to interact with Vertex AI.
- Camera input requires appropriate browser permissions.
- Session state data is cleared when the app restarts.

## License

This project is licensed under the [MIT License](LICENSE).
