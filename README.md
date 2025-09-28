# Mental Health Fitness Tracker

A modern web application for analyzing mental health data using machine learning. This application allows users to upload CSV files containing mental health data and generates comprehensive analysis including data visualizations, statistical insights, and machine learning model performance metrics.

## Features

- 📊 **Data Upload**: Upload two CSV files (mental disorders and substance use data)
- 🤖 **Machine Learning**: Automatic Random Forest model training and evaluation
- 📈 **Visualizations**: Interactive correlation heatmaps and pair plots
- 📱 **Responsive Design**: Modern, mobile-friendly interface
- 🎯 **Real-time Analysis**: Instant processing and results display
- 📋 **Comprehensive Statistics**: Detailed data insights and model performance metrics

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Machine Learning**: scikit-learn, pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Styling**: Custom CSS with gradient designs

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your web browser and navigate to `http://localhost:5000`

## Usage

### 1. Data Preparation

Prepare two CSV files with the following structure:

**File 1 - Mental Disorders Data:**
- Entity (Country name)
- Code (Country code)
- Year
- DALYs (Disability-Adjusted Life Years) - Mental disorders data

**File 2 - Substance Use Data:**
- Entity (Country name)
- Code (Country code)
- Year
- Prevalence data for various disorders (Schizophrenia, Bipolar, Eating disorders, Anxiety, Drug use, Depression, Alcohol use)

### 2. Upload and Analyze

1. Open the web application in your browser
2. Click "Choose File" for both CSV upload fields
3. Select your prepared CSV files
4. Click "Analyze Data" to start processing
5. Wait for the analysis to complete (this may take a few moments)
6. View the results including:
   - Data statistics
   - Model performance metrics
   - Correlation heatmap
   - Data pairplot

### 3. Understanding the Results

- **Statistics**: Overview of your dataset including record count, mean values, and data distribution
- **Model Performance**: Training and testing metrics for the Random Forest model
- **Correlation Heatmap**: Shows relationships between different mental health indicators
- **Pairplot**: Detailed scatter plots showing data distributions and correlations

## File Structure

```
Mental_Health_Fitness_Tracker/
├── app.py                          # Flask backend application
├── requirements.txt                 # Python dependencies
├── templates/
│   └── index.html                  # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css              # Custom CSS styling
│   └── js/
│       └── app.js                 # Frontend JavaScript
├── uploads/                       # Directory for uploaded files
├── Mental_Fitness_Tracker.ipynb   # Original Jupyter notebook
├── mental-and-substance-use-as-share-of-disease.csv
├── prevalence-by-mental-and-substance-use-disorder.csv
└── README.md                      # This file
```

## API Endpoints

- `GET /` - Main application page
- `POST /api/upload` - Upload and process CSV files
- `POST /api/predict` - Make predictions (future feature)

## Data Processing Pipeline

1. **Data Merging**: Combines the two uploaded CSV files
2. **Data Cleaning**: Removes missing values and unnecessary columns
3. **Feature Engineering**: Renames columns and encodes categorical variables
4. **Model Training**: Trains a Random Forest regressor
5. **Visualization**: Generates correlation heatmaps and pair plots
6. **Results**: Returns comprehensive analysis results

## Model Performance

The application uses a Random Forest Regressor with the following typical performance:
- **Training R²**: ~99.9%
- **Testing R²**: ~99.5%
- **Low RMSE**: Indicates high prediction accuracy

## Customization

### Adding New Visualizations

To add new visualizations, modify the `app.py` file:

```python
def create_custom_visualization(df):
    # Your visualization code here
    plt.figure(figsize=(10, 6))
    # ... plotting code ...
    return img_base64
```

### Modifying the Model

To use a different machine learning model, update the `train_model` function in `app.py`:

```python
from sklearn.linear_model import LinearRegression
# Replace RandomForestRegressor with your preferred model
```

## Troubleshooting

### Common Issues

1. **File Upload Errors**:
   - Ensure files are in CSV format
   - Check file size (max 16MB)
   - Verify required columns are present

2. **Processing Errors**:
   - Check that both files have matching Entity, Code, and Year columns
   - Ensure no critical data is missing

3. **Visualization Issues**:
   - Make sure matplotlib backend is properly configured
   - Check that data contains numeric values for plotting

### Performance Tips

- For large datasets, consider sampling the data
- Ensure sufficient RAM for processing large files
- Close other applications to free up system resources

## Contributing

Feel free to contribute to this project by:
- Adding new visualization types
- Implementing additional machine learning models
- Improving the user interface
- Adding new data processing features

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the console output for error messages
3. Ensure all dependencies are properly installed

## Future Enhancements

- [ ] Real-time prediction interface
- [ ] Export results to PDF/Excel
- [ ] Advanced filtering options
- [ ] Multiple model comparison
- [ ] Interactive 3D visualizations
- [ ] Data export functionality
