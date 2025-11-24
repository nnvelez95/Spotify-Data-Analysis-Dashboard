import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import json

class GlobalMusicAnalyzer:
    def __init__(self):
        self.genres = ['Pop', 'Rock', 'Hip-Hop', 'Electronic', 'R&B', 'Country', 'Jazz', 'Classical', 'Reggaeton', 'K-Pop']
        self.countries = ['Global', 'US', 'UK', 'Japan', 'Brazil', 'Germany', 'France', 'Mexico', 'India', 'Australia']
        
    def get_global_charts_data(self):
        """Datos simulados de charts globales - MUCHO más realistas"""
        # Artistas populares actuales
        popular_artists = {
            'Pop': ['Taylor Swift', 'Dua Lipa', 'Ed Sheeran', 'Ariana Grande', 'Harry Styles'],
            'Rock': ['Arctic Monkeys', 'Imagine Dragons', 'The Rolling Stones', 'Foo Fighters', 'Muse'],
            'Hip-Hop': ['Drake', 'Kendrick Lamar', 'Travis Scott', 'Cardi B', 'Post Malone'],
            'Electronic': ['Calvin Harris', 'David Guetta', 'The Chainsmokers', 'Marshmello', 'Swedish House Mafia'],
            'R&B': ['The Weeknd', 'SZA', 'Bruno Mars', 'H.E.R.', 'Summer Walker'],
            'Reggaeton': ['Bad Bunny', 'J Balvin', 'Karol G', 'Rauw Alejandro', 'Anuel AA'],
            'K-Pop': ['BTS', 'BLACKPINK', 'TWICE', 'Stray Kids', 'NewJeans']
        }
        
        data = []
        track_id = 0
        
        for genre in self.genres:
            artists = popular_artists.get(genre, ['Various Artists'])
            
            for i, artist in enumerate(artists):
                for week in range(4):  # 4 semanas de datos
                    track_id += 1
                    # Popularidad basada en posición y tiempo
                    base_popularity = 100 - (i * 5) - (week * 2)
                    
                    # Características por género (muy realistas)
                    genre_features = self._get_genre_features(genre)
                    
                    data.append({
                        'track_id': track_id,
                        'track_name': f"{self._generate_track_name(artist, genre)}",
                        'artist': artist,
                        'genre': genre,
                        'country': 'Global',
                        'popularity': max(60, base_popularity + np.random.randint(-10, 10)),
                        'streams_millions': np.random.randint(50, 500),
                        'week': f"2024-{12-week:02d}-01",
                        'duration_min': round(np.random.uniform(2.5, 4.5), 2),
                        'danceability': max(0.1, min(0.95, genre_features['danceability'] + np.random.uniform(-0.2, 0.2))),
                        'energy': max(0.1, min(0.95, genre_features['energy'] + np.random.uniform(-0.15, 0.15))),
                        'valence': max(0.1, min(0.95, genre_features['valence'] + np.random.uniform(-0.15, 0.15))),
                        'acousticness': max(0.01, min(0.95, genre_features['acousticness'] + np.random.uniform(-0.1, 0.1))),
                        'instrumentalness': max(0.0, min(0.8, genre_features['instrumentalness'] + np.random.uniform(-0.1, 0.1))),
                        'tempo': max(60, min(180, genre_features['tempo'] + np.random.randint(-10, 10))),
                        'loudness': np.random.uniform(-12, -4),
                        'speechiness': max(0.02, min(0.3, genre_features['speechiness'] + np.random.uniform(-0.05, 0.05))),
                    })
        
        return pd.DataFrame(data)
    
    def _get_genre_features(self, genre):
        """Características de audio típicas por género"""
        features = {
            'Pop': {'danceability': 0.75, 'energy': 0.70, 'valence': 0.65, 
                   'acousticness': 0.15, 'instrumentalness': 0.02, 'tempo': 120, 'speechiness': 0.05},
            'Rock': {'danceability': 0.55, 'energy': 0.85, 'valence': 0.50,
                    'acousticness': 0.25, 'instrumentalness': 0.10, 'tempo': 130, 'speechiness': 0.04},
            'Hip-Hop': {'danceability': 0.80, 'energy': 0.65, 'valence': 0.45,
                       'acousticness': 0.08, 'instrumentalness': 0.01, 'tempo': 95, 'speechiness': 0.25},
            'Electronic': {'danceability': 0.85, 'energy': 0.80, 'valence': 0.60,
                         'acousticness': 0.05, 'instrumentalness': 0.15, 'tempo': 128, 'speechiness': 0.03},
            'R&B': {'danceability': 0.70, 'energy': 0.60, 'valence': 0.55,
                   'acousticness': 0.20, 'instrumentalness': 0.03, 'tempo': 90, 'speechiness': 0.08},
            'Country': {'danceability': 0.60, 'energy': 0.65, 'valence': 0.70,
                       'acousticness': 0.45, 'instrumentalness': 0.05, 'tempo': 110, 'speechiness': 0.06},
            'Jazz': {'danceability': 0.45, 'energy': 0.40, 'valence': 0.50,
                    'acousticness': 0.85, 'instrumentalness': 0.25, 'tempo': 115, 'speechiness': 0.03},
            'Classical': {'danceability': 0.25, 'energy': 0.30, 'valence': 0.40,
                         'acousticness': 0.95, 'instrumentalness': 0.80, 'tempo': 100, 'speechiness': 0.01},
            'Reggaeton': {'danceability': 0.90, 'energy': 0.75, 'valence': 0.70,
                         'acousticness': 0.10, 'instrumentalness': 0.02, 'tempo': 95, 'speechiness': 0.15},
            'K-Pop': {'danceability': 0.80, 'energy': 0.85, 'valence': 0.75,
                     'acousticness': 0.12, 'instrumentalness': 0.04, 'tempo': 125, 'speechiness': 0.07}
        }
        return features.get(genre, features['Pop'])
    
    def _generate_track_name(self, artist, genre):
        """Generar nombres de canciones realistas"""
        pop_titles = ['Dancing in the Moonlight', 'Electric Dreams', 'Midnight City', 'Golden Hour', 'Summer Vibes']
        rock_titles = ['Thunder Road', 'Mountain High', 'Electric Storm', 'Rebel Heart', 'Free Fallin']
        hiphop_titles = ['King\'s Gambit', 'Street Dreams', 'All Eyes On Me', 'Top of the Game', 'Legacy']
        electronic_titles = ['Neon Pulse', 'Digital Dreams', 'Echo Chamber', 'Synthetic Love', 'Future Bass']
        rnb_titles = ['Midnight Drive', 'Smooth Operator', 'Velvet Touch', 'City Lights', 'Quiet Storm']
        country_titles = ['Dusty Road', 'Whiskey River', 'Small Town', 'Blue Skies', 'Backroads']
        jazz_titles = ['Midnight Blues', 'Smooth Jazz', 'City Nights', 'Quiet Moments', 'Cool Breeze']
        classical_titles = ['Moonlight Sonata', 'Winter Prelude', 'Spring Symphony', 'Nocturne', 'Adagio']
        reggaeton_titles = ['Baila Conmigo', 'Fiesta', 'Calor', 'Ritmo', 'Dale']
        kpop_titles = ['Fire', 'Dreams', 'Star', 'Love Shot', 'Butterfly']
        
        genre_titles = {
            'Pop': pop_titles,
            'Rock': rock_titles,
            'Hip-Hop': hiphop_titles,
            'Electronic': electronic_titles,
            'R&B': rnb_titles,
            'Country': country_titles,
            'Jazz': jazz_titles,
            'Classical': classical_titles,
            'Reggaeton': reggaeton_titles,
            'K-Pop': kpop_titles
        }
        
        titles = genre_titles.get(genre, pop_titles)
        return f"{np.random.choice(titles)}"
    
    def get_genre_comparison(self):
        """Análisis comparativo entre géneros"""
        df = self.get_global_charts_data()
        genre_stats = df.groupby('genre').agg({
            'popularity': 'mean',
            'danceability': 'mean',
            'energy': 'mean',
            'valence': 'mean',
            'acousticness': 'mean',
            'tempo': 'mean',
            'streams_millions': 'sum'
        }).round(3)
        
        return genre_stats
    
    def get_artist_analysis(self):
        """Análisis por artista"""
        df = self.get_global_charts_data()
        artist_stats = df.groupby('artist').agg({
            'popularity': 'mean',
            'streams_millions': 'sum',
            'danceability': 'mean',
            'energy': 'mean',
            'genre': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Unknown'
        }).round(3).sort_values('streams_millions', ascending=False)
        
        return artist_stats

# Instancia global
music_analyzer = GlobalMusicAnalyzer()