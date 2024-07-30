Here is a concise description for your project on GitHub:

---

## Denial Analysis Web Application

This project is a web application designed to analyze denial records from CSV files. It processes daily CSV uploads, stores the data in an SQLite database, and provides a web interface for visualization and analysis.

### Features

1. **CSV File Upload**: Upload daily CSV files containing denial records.
2. **Data Storage**: Records are stored in an SQLite database.
3. **Visualization**: View the terminals with the most denials from the latest upload and summaries of denials over the last 7 days.
4. **Detailed View**: Clickable rows for detailed denial records by terminal.
5. **Duplicate Check**: Alerts for duplicate file uploads.
6. **Responsive Design**: User-friendly interface built with Bootstrap.

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/denial-analysis-webapp.git
    cd denial-analysis-webapp
    ```

2. Install dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python3 app.py
    ```

4. Access the app at `http://127.0.0.1:5000`.

### Usage

1. **Upload a CSV File**: Use the form to upload a CSV file.
2. **View Summaries**: See summaries of denials from the latest upload and the past 7 days.
3. **View Details**: Click on a row for detailed denial records by terminal.

### License

Licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to adjust the description as needed.
