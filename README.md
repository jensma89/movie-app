# Movie App

A simple command-line based Movie App that allows you to manage your personal movie collection using the OMDb API. The app fetches movie details from the internet, stores them in a local SQLite database, and can generate a clean HTML page to display your collection.

---

## Features

- **Add movie** from the OMDb API  
- **List movies** in the local database  
- **Update movie rating**  
- **Delete movie**  
- **View movie statistics** (year, title, rating)  
- **Get a random movie**  
- **Search movies** by title (supports partial matches)  
- **Sort movies by rating**  
- **Generate a website** (`index.html`) displaying your collection  

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/movie-app.git
cd movie-app
```

### 2. Install dependencies

Make sure you have Python 3 installed, then run:

```bash
pip install -r requirements.txt
```

### 3. Get your OMDb API Key

- Go to [http://www.omdbapi.com/apikey.aspx](http://www.omdbapi.com/apikey.aspx)  
- Register for a free API key  
- Create a `.env` file in the root of the project and paste your key like this:

```
OMDB_API_KEY=your_api_key_here
```

Example:

```
OMDB_API_KEY=example1234
```

---

## Usage

Run the main script:

```bash
python main.py
```

You will be prompted with a menu of options. Some key commands:

- `add movie`: Add a movie by title (fetches data from OMDb)  
- `list movies`: Lists all movies currently stored  
- `update movie`: Update a movie's rating  
- `delete movie`: Remove a movie from the collection  
- `movie stats`: Shows statistics like average rating, best/worst movies  
- `random movie`: Returns a random movie  
- `search movie`: Search for a movie by partial or full title  
- `movies sorted by rating`: Shows all movies sorted by rating  
- `generate website`: Generates a file `index.html` that displays all movies in a styled webpage  

The generated HTML file will be saved in the root directory and can be opened in any web browser.

---

## Data Storage

The movie data is stored locally using SQLite. The database file `movies.db` is automatically created in the `data/` directory.