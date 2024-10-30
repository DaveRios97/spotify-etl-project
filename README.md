# Spotify ETL Project

## Description
A Spotify ETL project is an starter data engineering project I'm doing to learn and improve the ETL process in the data engineering world.

## Authors
- **[David (Dave) Rios](https://github.com/DaveRios97)** - *Backend Software Developer seeking a position as a Data Engineer or Data Analyst*

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Sources](#data-sources)
- [Contributing](#contributing)
- [License](#license)

## Installation

To set up and run this project, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/DaveRios97/spotify-etl-project.git
```

### 2. Create the `.env` File.

Navigate to the root directory of the project and create a file named `.env`. Add the following environment variables:

```
CLIENT_ID           required for spotipy
CLIENT_SECRET       required for spotipy

DB_USER             required for Docker Postgres DB
DB_PASSWORD         required for Docker Postgres DB
DB_HOSY             required for Docker Postgres DB
DB_PORT             required for Docker Postgres DB
DB_NAME             required for Docker Postgres DB
```

### 3. Start the Docker Compose
Ensure that [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/) are installed. In your terminal, navigate to the root directory of the project and run:

```bash
docker-compose up -d
```

### 4. Create a Python Virtual Environment

In the project root directory, create a virtual environment. Run the following commands:

```bash
# On Unix or macOS
python3 -m venv venv

# On Windows
python -m venv venv
```

### 5. Activate the Virtual Environment

Activate the virtual environment:

```bash
# On Unix or macOS
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 6. Install Dependencies

With the virtual environment activated, install the dependencies required by the project:

```bash
pip install -r requirements.txt
```

## Usage
Run the application to initiate the ETL process by executing the following command:

```bash
python main.py
```

After running this, the extracted data will be loaded into your database. You may use [DBEaver](https://dbeaver.io/) to visualize and explore the data in the database.

---

## Project Structure

### The project is organized as follows:

```
├── .gitignore 
├── docker-compose.yaml
├── main.py
├── README.md
├── requirements.txt
```

### Description of each file:

- **.gitignore**: Specifies files and directories for Git to ignore, such as the virtual environment and sensitive files.
- **docker-compose.yaml**: Docker configuration file that defines and manages containers needed for the project, such as the database.
- **main.py**: Contains the code to run the ETL process in an automated way.
- **README.md**: Reference document with installation instructions, project structure, and usage guide.
- **requirements.txt**: Contains all the Python libraries needed for the project to function.