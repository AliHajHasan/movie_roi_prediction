# 🎬 Movie Income Prediction using Machine Learning  

## 📌 Overview  
This project aims to **predict movie revenues** using machine learning techniques. By collecting and preprocessing data from multiple online sources (e.g., IMDb and Box Office Mojo), we developed predictive models to estimate box office performance and analyze the factors that drive a movie’s success.  

---

## ⚙️ Project Workflow  

1. **Data Collection**  
   - Scraped data from:  
     - [IMDb](https://www.imdb.com/) – movie metadata (title, release date, genres, ratings, cast, etc.)  
     - [Box Office Mojo](https://www.boxofficemojo.com/) – box office revenue figures.  
   - Implemented web scraping using **BeautifulSoup**, **Selenium**, and **Requests**.  

2. **Data Preprocessing**  
   - Cleaned raw data (removed duplicates, handled missing values).  
   - Merged IMDb and Box Office Mojo datasets into a unified database.  
   - Engineered features such as:  
     - Genre encoding (multi-label handling).  
     - Cast/crew indicators.  
     - Budget vs. revenue ratios.  
     - Release month/season features.  

3. **Exploratory Data Analysis (EDA)**  
   - Identified correlations between revenue and features like budget, IMDb rating, and genre.  
   - Visualized distributions and patterns using **Matplotlib** and **Seaborn**.  

4. **Modeling**  
   - Applied multiple regression algorithms to predict revenue:  
     - Linear Regression  
     - Random Forest Regressor  
     - XGBoost Regressor  
   - Evaluated models using **MAE**, **RMSE**, and **R²**.  

---

## 🛠️ Tech Stack  

- **Languages**: Python  
- **Libraries**: Pandas, NumPy, Scikit-learn, XGBoost, BeautifulSoup, Selenium, Requests, Matplotlib, Seaborn  
- **Tools**: Jupyter Notebook, GitHub  

---



