from flask import render_template, request, redirect, url_for, flash
from .file_processing import process_file, calculate_file_hash
from .utils import get_latest_upload_data, get_denegations_last_7_days, get_details_for_box, get_latest_file_hash
from .database import save_to_db, check_file_hash_exists

def configure_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part', 'danger')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file', 'danger')
                return redirect(request.url)
            if file:
                file_hash = calculate_file_hash(file)
                if check_file_hash_exists(file_hash):
                    flash('Archivo ya ha sido subido previamente.', 'danger')
                else:
                    df = process_file(file)
                    save_to_db(df, file_hash)
                    flash('Archivo subido y procesado correctamente.', 'success')
        
        last_7_days_data = get_denegations_last_7_days()
        latest_file_hash = get_latest_file_hash()
        latest_upload_data = get_latest_upload_data(latest_file_hash) if latest_file_hash else []
        column_names = [col for col in last_7_days_data[0].keys() if col not in ['Centro', 'Caja', 'Total']] if last_7_days_data else []

        return render_template('summary.html', last_7_days_data=last_7_days_data, latest_upload_data=latest_upload_data, column_names=column_names)

    @app.route('/details/<centro>/<caja>')
    def details(centro, caja):
        details_data = get_details_for_box(centro, caja)
        return render_template('details.html', details_data=details_data, centro=centro, caja=caja)
