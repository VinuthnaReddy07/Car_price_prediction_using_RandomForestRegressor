# AutoValue: Car Price Prediction

A machine learning project that predicts used car selling prices from vehicle details such as brand, model, year, fuel type, transmission, mileage, and ownership history.

This project includes:
- a training script to build the prediction model
- a Streamlit web app for interactive price estimation
- a saved model artifact and evaluation plot

## Project overview

The model is trained using a used-car dataset and a RandomForest regressor with preprocessing for categorical fields. The trained model is then saved as `car_price_model.pkl` and used by the Streamlit app in `app.py`.

## Project files

- `Car_price_prediction.py` — loads the dataset, trains the model, evaluates it, and saves the model artifact.
- `app.py` — interactive web app for entering vehicle details and getting a price estimate.
- `car_price_model.pkl` — trained model and metadata used by the app.
- `car_price_predictions.png` — scatter plot showing actual vs predicted prices.

## Prerequisites

- Python 3.9+
- pip

## Setup

Install the required Python packages:

```bash
pip install pandas scikit-learn joblib matplotlib streamlit
```

Place the dataset file at:

```text
C:\Users\<your-user>\Downloads\Car details v3.csv
```

The training script reads the dataset from the user's Downloads folder.

## Train the model

Run:

```bash
python Car_price_prediction.py
```

This will:
- load the dataset
- preprocess the data
- train a RandomForest model
- print evaluation metrics like MAE and R2 score
- save `car_price_model.pkl`
- save `car_price_predictions.png`

## Run the web app

Start the Streamlit app:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (typically `http://localhost:8501`).

## How the app works

Users can enter:
- brand
- model
- manufacturing year
- kilometers driven
- fuel type
- transmission
- number of previous owners
- mileage

The app passes these inputs to the trained model and displays the estimated selling price.

## Notes

- The estimate is a model-based approximation and should be treated as a guidance value, not a guaranteed market price.
- If `car_price_model.pkl` is missing, run `Car_price_prediction.py` before launching the app.

## License

This project is provided for educational and demo purposes.
