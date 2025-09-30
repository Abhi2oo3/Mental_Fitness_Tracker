from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os

# Set matplotlib cache directory for Render
os.environ['MPLCONFIGDIR'] = os.environ.get('MPLCONFIGDIR', '/tmp/matplotlib')
import seaborn as sns
import io
import base64
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_mental_health_data(df1, df2):
    """Process mental health data similar to the notebook logic"""
    try:
        # Merge the datasets
        df = pd.merge(df1, df2, on=['Entity', 'Year', 'Code'])
        
        # Remove rows with missing values
        df = df.dropna()
        
        # Drop the Code column
        df = df.drop("Code", axis=1)
        
        # Rename columns for better readability
        column_mapping = {
            'Entity': 'Country',
            'Year': 'Year',
            'DALYs (Disability-Adjusted Life Years) - Mental disorders - Sex: Both - Age: All Ages (Percent)': 'mental_fitness',
            'Prevalence - Schizophrenia - Sex: Both - Age: Age-standardized (Percent)': 'Schizophrenia',
            'Prevalence - Bipolar disorder - Sex: Both - Age: Age-standardized (Percent)': 'Bipolar_disorder',
            'Prevalence - Eating disorders - Sex: Both - Age: Age-standardized (Percent)': 'Eating_disorder',
            'Prevalence - Anxiety disorders - Sex: Both - Age: Age-standardized (Percent)': 'Anxiety',
            'Prevalence - Drug use disorders - Sex: Both - Age: Age-standardized (Percent)': 'drug_usage',
            'Prevalence - Depressive disorders - Sex: Both - Age: Age-standardized (Percent)': 'depression',
            'Prevalence - Alcohol use disorders - Sex: Both - Age: Age-standardized (Percent)': 'alcohol'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Encode categorical variables (but preserve Year as numeric)
        le = LabelEncoder()
        for col in df.columns:
            if df[col].dtype == 'object' and col != 'Year':
                df[col] = le.fit_transform(df[col])
        
        # Ensure Year is numeric
        if 'Year' in df.columns:
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        
        return df, None
    except Exception as e:
        return None, str(e)

def train_model(df):
    """Train the Random Forest model"""
    try:
        X = df.drop('mental_fitness', axis=1)
        y = df['mental_fitness']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
        
        rf = RandomForestRegressor()
        rf.fit(X_train, y_train)
        
        # Model evaluation
        y_train_pred = rf.predict(X_train)
        y_test_pred = rf.predict(X_test)
        
        train_mse = mean_squared_error(y_train, y_train_pred)
        train_rmse = np.sqrt(train_mse)
        train_r2 = r2_score(y_train, y_train_pred)
        
        test_mse = mean_squared_error(y_test, y_test_pred)
        test_rmse = np.sqrt(test_mse)
        test_r2 = r2_score(y_test, y_test_pred)
        
        return {
            'model': rf,
            'train_metrics': {
                'mse': train_mse,
                'rmse': train_rmse,
                'r2': train_r2
            },
            'test_metrics': {
                'mse': test_mse,
                'rmse': test_rmse,
                'r2': test_r2
            }
        }, None
    except Exception as e:
        return None, str(e)

def create_correlation_heatmap(df):
    """Create correlation heatmap"""
    try:
        plt.figure(figsize=(12, 8))
        correlation_matrix = df.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='Blues', center=0)
        plt.title('Mental Health Data Correlation Matrix')
        plt.tight_layout()
        
        # Convert plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_base64
    except Exception as e:
        print(f"Error creating correlation heatmap: {e}")
        return None

def create_pairplot(df):
    """Create pairplot for data visualization"""
    try:
        plt.figure(figsize=(15, 12))
        
        # Select numeric columns for pairplot
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df_numeric = df[numeric_cols]
        
        # Create pairplot
        sns.pairplot(df_numeric, corner=True)
        plt.suptitle('Mental Health Data Pairplot', y=1.02)
        plt.tight_layout()
        
        # Convert plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_base64
    except Exception as e:
        print(f"Error creating pairplot: {e}")
        return None

def create_distribution_histogram(df):
    """Create distribution histogram for mental health indicators"""
    try:
        # Select key mental health indicators
        key_indicators = ['mental_fitness', 'depression', 'anxiety', 'drug_usage', 'alcohol']
        available_indicators = [col for col in key_indicators if col in df.columns]
        
        if not available_indicators:
            return None
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()
        
        for i, indicator in enumerate(available_indicators[:6]):
            if i < len(axes):
                axes[i].hist(df[indicator], bins=30, alpha=0.7, color=plt.cm.viridis(i/len(available_indicators)), edgecolor='black')
                axes[i].set_title(f'{indicator.replace("_", " ").title()} Distribution', fontsize=12, fontweight='bold')
                axes[i].set_xlabel('Value')
                axes[i].set_ylabel('Frequency')
                axes[i].grid(True, alpha=0.3)
                
                # Add statistics
                mean_val = df[indicator].mean()
                std_val = df[indicator].std()
                axes[i].axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.3f}')
                axes[i].axvline(mean_val + std_val, color='orange', linestyle=':', alpha=0.7, label=f'±1σ: {std_val:.3f}')
                axes[i].axvline(mean_val - std_val, color='orange', linestyle=':', alpha=0.7)
                axes[i].legend(fontsize=8)
        
        # Hide unused subplots
        for i in range(len(available_indicators), len(axes)):
            axes[i].set_visible(False)
        
        plt.suptitle('Mental Health Indicators Distribution Analysis', fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        
        # Convert plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_base64
    except Exception as e:
        print(f"Error creating distribution histogram: {e}")
        return None

def create_time_series_analysis(df):
    """Create time series analysis showing trends over years"""
    try:
        # Check if Year column exists and has enough data
        if 'Year' not in df.columns:
            print("Year column not found in data")
            return None
        
        # Remove any rows with invalid year data
        df_clean = df.dropna(subset=['Year']).copy()
        if len(df_clean) == 0:
            print("No valid year data found")
            return None
        
        # Ensure Year is numeric and has enough unique values
        df_clean['Year'] = pd.to_numeric(df_clean['Year'], errors='coerce')
        df_clean = df_clean.dropna(subset=['Year'])
        
        if df_clean['Year'].nunique() < 2:
            print(f"Not enough unique years for time series analysis. Found: {df_clean['Year'].nunique()}")
            return None
        
        # Group by year and calculate mean values for available columns
        available_columns = ['mental_fitness', 'depression', 'anxiety', 'drug_usage', 'alcohol']
        existing_columns = [col for col in available_columns if col in df_clean.columns]
        
        if not existing_columns:
            print("No suitable columns found for time series analysis")
            return None
        
        yearly_data = df_clean.groupby('Year')[existing_columns].mean().reset_index()
        
        # Create subplots based on available data
        num_plots = min(len(existing_columns), 4)
        if num_plots == 1:
            fig, axes = plt.subplots(1, 1, figsize=(12, 8))
            axes = [axes]
        elif num_plots == 2:
            fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        else:
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            axes = axes.flatten()
        
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E', '#7209B7']
        markers = ['o', 's', '^', 'D', 'v', 'p']
        
        # Plot available data
        for i, col in enumerate(existing_columns[:num_plots]):
            if i < len(axes):
                axes[i].plot(yearly_data['Year'], yearly_data[col], 
                           marker=markers[i % len(markers)], 
                           linewidth=3, markersize=8, 
                           color=colors[i % len(colors)],
                           label=col.replace('_', ' ').title())
                axes[i].set_title(f'{col.replace("_", " ").title()} Trend Over Time', 
                                fontsize=14, fontweight='bold')
                axes[i].set_xlabel('Year')
                axes[i].set_ylabel('Value')
                axes[i].grid(True, alpha=0.3)
                axes[i].fill_between(yearly_data['Year'], yearly_data[col], 
                                   alpha=0.3, color=colors[i % len(colors)])
                
                # Add trend line
                z = np.polyfit(yearly_data['Year'], yearly_data[col], 1)
                p = np.poly1d(z)
                axes[i].plot(yearly_data['Year'], p(yearly_data['Year']), 
                           "--", alpha=0.8, color='red', linewidth=2, label='Trend')
                axes[i].legend()
        
        # Hide unused subplots
        for i in range(len(existing_columns), len(axes)):
            axes[i].set_visible(False)
        
        plt.suptitle('Mental Health Trends Analysis Over Time', fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        
        # Convert plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_base64
    except Exception as e:
        print(f"Error creating time series analysis: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_feature_importance_chart(df, model):
    """Create feature importance chart from the trained model"""
    try:
        # Get feature importance from the model
        feature_names = [col for col in df.columns if col != 'mental_fitness']
        importance_scores = model.feature_importances_
        
        # Create DataFrame for better handling
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importance_scores
        }).sort_values('Importance', ascending=True)
        
        # Create horizontal bar chart
        plt.figure(figsize=(12, 8))
        colors = plt.cm.viridis(np.linspace(0, 1, len(importance_df)))
        
        bars = plt.barh(importance_df['Feature'], importance_df['Importance'], color=colors)
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, importance_df['Importance'])):
            plt.text(value + 0.001, bar.get_y() + bar.get_height()/2, 
                    f'{value:.3f}', va='center', fontweight='bold')
        
        plt.title('Feature Importance in Mental Fitness Prediction', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Importance Score', fontsize=12)
        plt.ylabel('Features', fontsize=12)
        plt.grid(True, alpha=0.3, axis='x')
        
        # Add percentage labels
        total_importance = importance_df['Importance'].sum()
        for i, (bar, value) in enumerate(zip(bars, importance_df['Importance'])):
            percentage = (value / total_importance) * 100
            plt.text(value/2, bar.get_y() + bar.get_height()/2, 
                    f'{percentage:.1f}%', va='center', ha='center', 
                    color='white', fontweight='bold', fontsize=10)
        
        plt.tight_layout()
        
        # Convert plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_base64
    except Exception as e:
        print(f"Error creating feature importance chart: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No content response for favicon

@app.route('/api/upload', methods=['POST'])
def upload_files():
    try:
        if 'file1' not in request.files or 'file2' not in request.files:
            return jsonify({'error': 'Two CSV files are required'}), 400
        
        file1 = request.files['file1']
        file2 = request.files['file2']
        
        if file1.filename == '' or file2.filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
            return jsonify({'error': 'Only CSV files are allowed'}), 400
        
        # Read CSV files
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        
        # Process data
        processed_df, error = process_mental_health_data(df1, df2)
        if error:
            return jsonify({'error': f'Data processing error: {error}'}), 400
        
        # Train model
        model_result, error = train_model(processed_df)
        if error:
            return jsonify({'error': f'Model training error: {error}'}), 400
        
        # Create visualizations
        heatmap_img = create_correlation_heatmap(processed_df)
        pairplot_img = create_pairplot(processed_df)
        distribution_img = create_distribution_histogram(processed_df)
        timeseries_img = create_time_series_analysis(processed_df)
        feature_importance_img = create_feature_importance_chart(processed_df, model_result['model'])
        
        # Handle visualization errors
        visualizations = {}
        if heatmap_img:
            visualizations['correlation_heatmap'] = heatmap_img
        if pairplot_img:
            visualizations['pairplot'] = pairplot_img
        if distribution_img:
            visualizations['distribution_histogram'] = distribution_img
        if timeseries_img:
            visualizations['time_series_analysis'] = timeseries_img
        if feature_importance_img:
            visualizations['feature_importance'] = feature_importance_img
        
        # Get basic statistics
        stats = {
            'shape': processed_df.shape,
            'columns': list(processed_df.columns),
            'mean_mental_fitness': float(processed_df['mental_fitness'].mean()),
            'std_mental_fitness': float(processed_df['mental_fitness'].std()),
            'min_mental_fitness': float(processed_df['mental_fitness'].min()),
            'max_mental_fitness': float(processed_df['mental_fitness'].max())
        }
        
        return jsonify({
            'success': True,
            'data': {
                'statistics': stats,
                'model_metrics': {
                    'train': model_result['train_metrics'],
                    'test': model_result['test_metrics']
                },
                'visualizations': visualizations
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # This would implement prediction logic using the trained model
        # For now, return a placeholder response
        return jsonify({
            'success': True,
            'prediction': 'Prediction functionality to be implemented'
        })
    except Exception as e:
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500

@app.route('/api/debug', methods=['POST'])
def debug_data():
    """Debug endpoint to check data processing"""
    try:
        if 'file1' not in request.files or 'file2' not in request.files:
            return jsonify({'error': 'Two CSV files are required'}), 400
        
        file1 = request.files['file1']
        file2 = request.files['file2']
        
        # Read CSV files
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        
        # Process data
        processed_df, error = process_mental_health_data(df1, df2)
        if error:
            return jsonify({'error': f'Data processing error: {error}'}), 400
        
        # Return debug information
        debug_info = {
            'original_df1_shape': df1.shape,
            'original_df2_shape': df2.shape,
            'processed_df_shape': processed_df.shape,
            'processed_df_columns': list(processed_df.columns),
            'processed_df_dtypes': {col: str(dtype) for col, dtype in processed_df.dtypes.items()},
            'year_column_info': {
                'exists': 'Year' in processed_df.columns,
                'unique_values': processed_df['Year'].nunique() if 'Year' in processed_df.columns else 0,
                'sample_values': processed_df['Year'].head().tolist() if 'Year' in processed_df.columns else []
            },
            'sample_data': processed_df.head().to_dict('records')
        }
        
        return jsonify({'success': True, 'debug_info': debug_info})
        
    except Exception as e:
        return jsonify({'error': f'Debug error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
