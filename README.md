# medical-dataset-preparation
Preparation and exploratory analysis of a cardiovascular medical dataset using Python.
# Medical Dataset Preparation and Analysis

## Project Overview

This project is dedicated to the preparation, cleaning, and exploratory analysis of a medical dataset related to cardiovascular diseases.  
The main goal is to demonstrate a complete and reproducible workflow for working with real medical tabular data using Python.

The project covers all key stages of data work:
- loading raw data,
- exploratory data analysis (EDA),
- data cleaning and normalization,
- feature engineering,
- basic statistical analysis,
- visualization of results.

The project was implemented as part of an academic (educational) practice.

---

## Project Goal

The goal of the project is to prepare a high-quality medical dataset suitable for further analysis by:
- detecting and correcting incorrect or unrealistic medical values,
- transforming raw measurements into interpretable features,
- analyzing differences between patient groups,
- producing tables and visualizations for reporting.

---

## Dataset Description

The project uses the dataset **`cardio_train.csv`**, which contains anonymized medical data of patients.

### Dataset characteristics:
- Medical and anthropometric measurements
- Binary target variable indicating cardiovascular disease

### Main features:
- `age` — age in days  
- `gender` — gender  
- `height` — height (cm)  
- `weight` — weight (kg)  
- `ap_hi` — systolic blood pressure  
- `ap_lo` — diastolic blood pressure  
- `cholesterol` — cholesterol level (categorical)  
- `gluc` — glucose level (categorical)  
- `smoke`, `alco`, `active` — lifestyle indicators  
- `cardio` — target variable (0 — no disease, 1 — disease)

During preprocessing, additional features are created:
- `age_years`
- `bmi` (Body Mass Index)
- `pulse_pressure`
- `hypertension`
- `obesity`

---

## Project Structure

