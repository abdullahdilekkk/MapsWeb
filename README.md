# 🌍 MapsWeb Django Application

Welcome to **MapsWeb**! A dynamic and beautifully crafted mapping web application built using the powerful Django framework combined with the styling flexibility of Tailwind CSS. 

This repository allows users to visualize country/city markers, upload map-related CSV files, pull OpenWeather API data, and more.

## ✨ Features
- **Map Visualizations:** Interactive mapping capabilities for countries, cities, CSV data, and metropolitan data via Django.
- **Tailwind Integration:** Clean, responsive, and maintainable user interface thanks to **Django Tailwind**.
- **Data Imports:** Custom admin integrations and models enabling CSV uploads and plotting of coordinate data.
- **Weather API Support:** Readily available hooks for fetching data using OpenWeather!

## 🚀 Setup & Installation

Below are the steps required to get your environment up and running. 

### Prerequisites
- Python 3.8+
- Node.js and NPM (Required for Tailwind compilation)

### 1. Clone the project
```bash
git clone https://github.com/abdullahdilekkk/MapsWeb.git
cd MapsWeb
```

### 2. Create the environment
It is strongly recommended to use a virtual environment.
```bash
# MacOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install packages
Install the required python packages using pip.
```bash
pip install -r requirements.txt
```

*(Note: If you don't have a `requirements.txt`, install `django`, `django-tailwind`, `python-decouple`, and any other dependencies used in the project via `pip install ...`)*

### 4. Create your Environment Variables
This project requires environment variables to run securely! Copy the example environment file and fill in your keys.
```bash
cp .env.example .env
```
Inside `.env`, ensure you supply valid inputs for:
- `OPENWEATHER_API_KEY`
- `SECRET_KEY`
- `DEBUG`

### 5. Install Tailwind & Frontend Dependencies
Move into the Django project containing the `manage.py` file and install Tailwind Node modules.
```bash
cd Demo
python manage.py tailwind install
```

### 6. Run Database Migrations
Prepare the local SQLite database layout.
```bash
python manage.py migrate
```

### 7. Run the Application
Finally, start up both the Django web server and your Tailwind process!
```bash
python manage.py tailwind start
# Note: You may need to run `python manage.py runserver` in a secondary terminal.
```

Visit the running application locally at `http://127.0.0.1:8000`.

## 🗂 Project Structure
The repository is structured primarily under the `Demo` folder:
- **`Demo/Demo/`:** Core Django settings and configurations.
- **`Demo/Map/`:** The main Mapping and logic Application.
- **`Demo/accounts/`:** Handles any basic authentication/user views.
- **`Demo/theme/`:** Dedicated Tailwind CSS Django application managing the `src` frontend files.
- **`Demo/csv/`:** Sample CSV data files.

## 🛑 Important Security Notice
Please make sure **never** to commit your local `.env` and `db.sqlite3` files to GitHub in future commits! Use `.gitignore` responsibly to keep APIs hidden!
