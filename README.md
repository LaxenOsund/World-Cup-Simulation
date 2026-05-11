# World Cup Simulation Project

This project aims to simulate an entire FIFA World Cup using historical national team data, Elo ratings, and Poisson distribution to predict match outcomes.

## Project Structure

The project is divided into several modules to handle data fetching, strength calculations, and goal simulations:

* **`datafetcher.py`**: Automatically fetches historical match data for international men's teams from a public data source. It filters out future matches and saves the results to `results.csv`.
* **`elo.py`**: Implements an Elo rating system tailored for international football.
    * Starting Elo is set to **1500**.
    * Accounts for **home field advantage** by adding 100 points to the home team's rating during calculations.
    * Dynamically updates team strengths after every match based on the result (win, draw, or loss).
* **`poisson.py`**: Contains the logic to calculate the probability of a specific scoreline based on the teams' expected goal averages using Poisson distribution. This serves as the core of the simulation engine.

## Roadmap

- [x] Data acquisition and storage.
- [x] Elo system implementation for historical ranking.
- [x] Poisson distribution logic for goal probabilities.
- [x] Group stage simulation engine.
- [x] Knockout stage simulation engine (including extra time/penalties).
- [x] Data visualization of the most likely tournament winners.
- [Done but can always be better] Tune Elo system to more accurately calculate Elo

## Installation & Usage

1.  **Install dependencies:**
    ```bash
    pip install pandas
    ```

2.  **Fetch the latest data:**
    Run the data fetcher to update `results.csv` with the latest international results:
    ```bash
    python datafetcher.py
    ```

3.  **Update Elo rankings:**
    Process the historical data to generate current team ratings:
    ```bash
    python elo.py
    ```

## Data Source
The data used in this project is sourced from a comprehensive collection of international football results dating back to 1872.
