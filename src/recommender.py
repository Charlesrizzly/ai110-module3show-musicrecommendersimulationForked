from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import pandas as pd

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Recommends top-k songs for a user using content-based filtering.
        """
        # Convert Song objects to dicts for scoring
        song_dicts = [
            {
                "id": s.id,
                "title": s.title,
                "artist": s.artist,
                "genre": s.genre,
                "mood": s.mood,
                "energy": s.energy,
                "tempo_bpm": s.tempo_bpm,
                "valence": s.valence,
                "danceability": s.danceability,
                "acousticness": s.acousticness,
            }
            for s in self.songs
        ]

        # Convert UserProfile to dict format
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

        # Score using functional logic
        scored = recommend_songs(user_prefs, song_dicts, k=k)

        # Map back to Song objects by ID
        song_id_map = {s.id: s for s in self.songs}
        result = []
        for song_dict, score, explanation in scored:
            song_obj = song_id_map[song_dict["id"]]
            result.append(song_obj)

        return result

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Explains why a song is recommended for a user.
        """
        reasons = []

        # Genre match
        if song.genre == user.favorite_genre:
            reasons.append(f"matches your favorite genre ({user.favorite_genre})")

        # Mood match
        if song.mood == user.favorite_mood:
            reasons.append(f"matches your mood preference ({user.favorite_mood})")

        # Energy proximity
        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff < 0.2:
            reasons.append("matches your preferred energy level")

        # Acousticness
        song_is_acoustic = song.acousticness > 0.5
        if user.likes_acoustic == song_is_acoustic:
            acoustic_pref = "acoustic" if user.likes_acoustic else "electronic"
            reasons.append(f"fits your preference for {acoustic_pref} sounds")

        if not reasons:
            return f"{song.title} may interest you based on its musical attributes."

        return f"We recommend {song.title} because it {', and it '.join(reasons)}."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    df = pd.read_csv(csv_path)
    return df.to_dict(orient="records")

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    Scores songs based on content-based filtering: genre, mood, energy, and acousticness.
    """
    scored_songs = []

    for song in songs:
        score = 0.0
        reasons = []

        # Genre match (weight: 0.35)
        if song["genre"] == user_prefs.get("genre"):
            score += 0.35
            reasons.append(f"matches your genre ({user_prefs.get('genre')})")

        # Mood match (weight: 0.30)
        if song["mood"] == user_prefs.get("mood"):
            score += 0.30
            reasons.append(f"matches your mood ({user_prefs.get('mood')})")

        # Energy proximity (weight: 0.25)
        target_energy = user_prefs.get("energy", 0.5)
        energy_diff = abs(song["energy"] - target_energy)
        energy_score = 0.25 * (1 - energy_diff)
        score += energy_score
        if energy_diff < 0.2:
            reasons.append("matches your energy level")

        # Acousticness preference (weight: 0.10)
        likes_acoustic = user_prefs.get("likes_acoustic", False)
        song_is_acoustic = song["acousticness"] > 0.5
        if likes_acoustic == song_is_acoustic:
            score += 0.10
            acoustic_pref = "acoustic" if likes_acoustic else "electronic"
            reasons.append(f"fits your {acoustic_pref} preference")

        explanation = ", ".join(reasons).capitalize() + "." if reasons else "No strong matches."
        scored_songs.append((song, score, explanation))

    # Sort by score descending and return top k
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    return scored_songs[:k]
