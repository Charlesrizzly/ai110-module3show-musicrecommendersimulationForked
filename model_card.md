# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**ContentMatch 1.0** — A content-based music recommender using song audio features and user taste profiles.  

---

## 2. Intended Use

**Purpose**: This is an educational simulator demonstrating how music streaming platforms like Spotify use content-based filtering to suggest songs a user might enjoy based on their musical taste profile.

**For whom**: Classroom exploration and learning—not intended for real production use. Students use it to understand how song attributes (genre, mood, energy) map to personalized recommendations.

**Key assumptions**:
- Users have a stable, learnable taste profile (favorite genre, mood, energy level, acousticness preference)
- Song audio features are representative and well-calibrated
- User preferences can be captured in four simple dimensions
- Past behavior accurately predicts future taste  

---

## 3. How the Model Works

**The Core Idea**: For each song in the catalog, we calculate a "match score" between the song's attributes and what we know about the user's taste. Songs with higher scores are recommended first.

**User Profile**: We capture a user in four dimensions:
1. **Favorite Genre** — the primary music category they prefer (e.g., pop, lofi, rock)
2. **Favorite Mood** — the emotional tone they seek (e.g., happy, chill, intense)
3. **Target Energy** — how energetic they want music (scale 0–1; 0 = calm, 1 = intense)
4. **Acousticness Preference** — whether they prefer acoustic/unplugged sounds or electronic/produced tracks

**Scoring Formula** (weighted sum of four signals):
- **Genre Match** (35% weight): +0.35 points if song genre = user favorite genre, else 0
- **Mood Match** (30% weight): +0.30 points if song mood = user favorite mood, else 0
- **Energy Proximity** (25% weight): Score = 0.25 × (1 − |song energy − user target|). Songs within 0.2 of target energy get bonus mention
- **Acousticness Alignment** (10% weight): +0.10 if song's acoustic nature (>0.5 acousticness = acoustic) matches user preference

**Why these weights?** Genre and mood are categorical dealbreakers—if you like pop, lofi recommendations feel less relevant. Energy bridges the gap because it exists on a spectrum and fine-tunes within a genre. Acousticness is a tiebreaker for distinguishing between similar songs.

**Ranking**: All songs are scored, sorted by score descending, and the top k (default k=5) are returned.

---

## 4. Data

**Catalog Size**: 10 songs (a toy dataset for classroom demonstration)

**Genres Represented** (7 total):
- Pop (2 songs: *Sunrise City*, *Gym Hero*)
- Lofi (2 songs: *Midnight Coding*, *Library Rain*)
- Rock (1 song: *Storm Runner*)
- Ambient (1 song: *Spacewalk Thoughts*)
- Jazz (1 song: *Coffee Shop Stories*)
- Synthwave (1 song: *Night Drive Loop*)
- Indie Pop (1 song: *Rooftop Lights*)

**Moods Represented** (6 total):
- happy, chill, intense, relaxed, moody, focused

**Audio Features** (all sourced from standardized music analysis APIs like Spotify's):
- **energy**: 0–1 scale (continuous); range in dataset: 0.28–0.93
- **valence**: 0–1 scale; musical positivity; range: 0.48–0.84
- **danceability**: 0–1 scale; how suitable for dancing; range: 0.41–0.88
- **acousticness**: 0–1 scale; degree of acoustic instrumentation; range: 0.05–0.92
- **tempo_bpm**: beats per minute; range: 60–152

**No changes made** to the original dataset—it was provided as-is.

**Missing Dimensions**:
- **Artist diversity**: Only 10 unique artists
- **Temporal trends**: No release date or popularity signal
- **Lyrical content**: No language, theme, or lyrical tone analysis
- **Cultural context**: No geographical or cultural preference dimensions
- **User interaction history**: No collaborative signals (what other similar users liked)  

---

## 5. Strengths

**Clear, Intuitive Ranking**: For users with strong genre preferences (e.g., "I like pop, happy, high-energy"), the model correctly elevates matching songs. A pop/happy user gets *Sunrise City* at the top—which is indeed pop + happy + high-energy.

**Energy as a Fine-Tuning Signal**: Within a preferred genre, energy effectively separates songs. Two pop songs can both score high on genre/mood, but a user seeking calm pop will rank *Rooftop Lights* (energy=0.76) above *Gym Hero* (energy=0.93) more reliably.

**Transparent Explanations**: The model provides human-readable explanations ("matches your genre, mood, and energy level"), making it easy to understand why a song was suggested.

**Balanced Weighting**: The 35%-30%-25%-10% split respects that categorical features (genre, mood) matter most while allowing continuous features (energy) to refine within categories, and acousticness to act as a tiebreaker.  

---

## 6. Limitations and Bias

**No Collaborative Signal**: The model ignores what other users liked. If User A (a hip-hop fan) and User B (a rock fan) both skip rock songs, the system has no way to learn this cross-user pattern. Spotify, by contrast, identifies users with similar taste and recommends songs to A that B enjoyed.

**Cold Start Problem**: A brand-new user with no profile data gets no good recommendations. The system assumes you can articulate four dimensions of taste upfront—but real users often discover music accidentally.

**Genre Imbalance**:
- Pop is overrepresented (2/10 songs)
- Rock, ambient, jazz, synthwave, indie pop are severely underrepresented (1 each)
- A user with indie preference finds only 1 match in the catalog

**Mood Underrepresentation**:
- "Happy" and "chill" appear 2–3 times each
- "Moody" and "relaxed" appear only once
- A relaxed user sees fewer options

**Energy Clustering**: Songs cluster at low (0.28–0.42) and high (0.82–0.93) energy, with a gap in the middle (0.75–0.82). A user targeting mid-range energy (0.5) finds poor matches.

**No Diversity in Results**: The top-5 recommendations might all be pop songs if the user loves pop—no algorithmic push toward variety or discovery.

**Acousticness Oversimplification**: The binary split (acoustic = >0.5 acousticness) ignores that a user might enjoy both full electric and full acoustic versions of the same genre.

**No Temporal Context**: Release date, trendiness, and user mood/context (time of day, activity) are ignored.  

---

## 7. Evaluation

**Test Profiles**:

1. **The Pop Fan**: `{genre: "pop", mood: "happy", energy: 0.8, likes_acoustic: false}`
   - Expected: *Sunrise City* (pop, happy, energy=0.82) ranked first
   - Result: ✓ Correct. *Sunrise City* scores 0.99 (matches genre, mood, energy, acousticness)

2. **The Lofi Coder**: `{genre: "lofi", mood: "chill", energy: 0.4, likes_acoustic: true}`
   - Expected: Lofi songs (*Midnight Coding*, *Library Rain*) dominate
   - Result: ✓ Both lofi songs rank in top 3 due to genre match and energy proximity

3. **The Rock Enthusiast**: `{genre: "rock", mood: "intense", energy: 0.9, likes_acoustic: false}`
   - Expected: *Storm Runner* (rock, intense, energy=0.91) ranked first
   - Result: ✓ Correct. *Storm Runner* dominates all other songs for this user

4. **The Acoustic Minimalist**: `{genre: "ambient", mood: "chill", energy: 0.3, likes_acoustic: true}`
   - Expected: *Spacewalk Thoughts* (ambient, chill, energy=0.28, acousticness=0.92) + highly acoustic jazz
   - Result: ✓ *Spacewalk Thoughts* scores highest; *Coffee Shop Stories* (jazz, acoustic) ranks high

**Observations**:
- **What worked**: Exact genre-mood matches strongly skew results, as intended
- **What surprised**: Energy proximity (25% weight) has significant influence even without genre match; a chill ambient fan gets jazz songs because both are acoustic and match energy
- **Edge case**: A user preferring electronic sounds but obscure genres (only 1 catalog match) gets diluted recommendations from other matches

**No quantitative metrics** were computed (precision@5, recall, etc.) because ground truth user preferences are not available in this simulation.

---

## 8. Future Work

**Hybrid Filtering**: Add collaborative signals by tracking user interactions (likes, skips, replays). If two users with similar taste profiles both love Song X, recommend it to both, even if Song X doesn't perfectly match the calculated profile.

**Expanded User Profile**: Include additional dimensions:
- `target_valence` (seek happy vs. sad music)
- `target_tempo` (prefer fast or slow beats)
- `preferred_artist_style` (explicit artist or artist similarity)
- `context` tags (workout, study, party, sleep)

**Diversity Re-Ranking**: After scoring, apply a post-processing step to ensure the top-5 includes genre/artist variety, preventing all recommendations from being the same artist.

**Learning from Feedback**: Implement a feedback loop where users rate recommendations, and the model adjusts weights (e.g., if a user rates all high-energy songs poorly, reduce energy weight).

**Expanded Dataset**: Add 100+ songs across underrepresented genres (indie, metal, classical, K-pop) to reduce bias and improve recommendations for niche taste profiles.

**Temporal Context**: Factor in time-of-day, day-of-week, or user activity (e.g., suggest higher-energy songs during exercise, calmer songs at night).

**Explanation Enhancement**: Provide feature-level explanations with comparisons ("*Sunrise City* is 18% more energetic than your typical preference, but matches your genre perfectly").  

---

## 9. Personal Reflection

Building this recommender revealed how much simplicity masks real complexity. At first, a weighted scoring formula feels intuitive—match genre, mood, energy—but in practice, the choice of weights (35%-30%-25%-10%) shapes everything. Increase mood to 40%, and a user gets different top-5. Small arithmetic decisions become editorial decisions about what matters in taste.

The most surprising insight was how content-based filtering alone feels limiting. With only 10 songs, exact matches are rare, so the model often recommends songs that "half-match" (good energy but wrong genre). Real platforms use collaborative filtering (what users like you enjoyed) to escape this trap. Spotify probably knows that users with your exact profile loved Song X even if the audio features are surprising—and that's wisdom you can't bake into a formula.

I also learned that *transparency matters*. Explaining "matches your genre, mood, and energy" makes users trust (or challenge) the system. Without explanations, recommendations feel magical or arbitrary. This taught me that building trust in AI requires showing your work.

Finally, this simulator changes how I listen to music. Now I notice the energy level, mood tag, and acousticness of songs—the very dimensions the model uses. I realize Spotify's recommendations are probably far richer (artist similarity, temporal trends, social signals) but also subtly shaped by engagement metrics and profits. Good models are powerful precisely because you don't see the machinery. This exercise made me hyperaware of it.  
