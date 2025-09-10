# Movie Recommendation System 🎬

A content-based movie recommendation system built using the TMDB (The Movie Database) dataset. This project suggests movies to users based on movie features like genres, cast, crew, and plot keywords.

## About the Project

As a 3rd year BTech student, I developed this recommendation system to understand how machine learning can be applied to solve real-world problems. The system analyzes movie metadata and finds similarities between films to provide personalized recommendations.

## Features

- **Content-Based Filtering**: Recommends movies based on movie features and user preferences
- **Similarity Analysis**: Uses cosine similarity to find movies with similar characteristics
- **Interactive Interface**: Simple and user-friendly movie recommendation interface
- **TMDB Integration**: Leverages comprehensive movie data from TMDB

## Dataset

The project uses the TMDB 5000 Movie Dataset which includes:

- **movies_metadata.csv**: Contains movie details like budget, genres, revenue, runtime, etc.
- **credits.csv**: Information about cast and crew for each movie
- **keywords.csv**: Plot keywords associated with each movie

*Dataset Source: [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)*

## Files Structure

```
movie-recommendation-system/
│
├── data/
│   ├── credits.csv
│   └── movies.csv
│
├── movie_recommendation_system.ipynb
└── README.md
```

## How It Works

1. **Data Preprocessing**: Clean and process the movie dataset
2. **Feature Engineering**: Extract and combine relevant features (genres, cast, crew, keywords)
3. **Vectorization**: Convert text features into numerical vectors using TF-IDF or Count Vectorizer
4. **Similarity Calculation**: Compute cosine similarity between movies
5. **Recommendation Generation**: Return top N similar movies for a given input

## Getting Started

### Prerequisites

```bash
pip install pandas numpy scikit-learn matplotlib seaborn jupyter
```

### Running the Project

1. Clone this repository
2. Download the TMDB dataset and place it in the `data/` folder
3. Open `movie_recommendation_system.ipynb` in Jupyter Notebook
4. Run all cells to train the model and get recommendations

## Sample Usage

```python
# Get movie recommendations
recommendations = get_recommendations('The Dark Knight', 5)
print(recommendations)
```

## Key Learnings

- Understanding different types of recommendation systems
- Data preprocessing and feature engineering techniques
- Working with large datasets and handling missing values
- Implementing similarity measures and machine learning concepts
- Text processing and vectorization methods

## Future Improvements

- [ ] Implement collaborative filtering
- [ ] Add hybrid recommendation approach
- [ ] Create a web interface using Flask/Streamlit
- [ ] Include movie ratings and user feedback
- [ ] Add more sophisticated NLP techniques

## Technologies Used

- **Python**: Main programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning library
- **Matplotlib/Seaborn**: Data visualization

## Acknowledgments

- Thanks to TMDB for providing the comprehensive movie dataset
- Tutorial reference: [YouTube Tutorial Link](https://www.youtube.com/watch?v=1xtrIEwY_zY&list=PLKnIA16_RmvY5eP91BGPa0vXUYmIdtfPQ)
- Inspiration from various online resources and documentation

## Contact

Feel free to reach out if you have any questions or suggestions!

---
*This project was developed as part of my BTech learning journey in Data Science and Machine Learning.*
