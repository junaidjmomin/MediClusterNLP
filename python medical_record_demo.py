import numpy as np
import pandas as pd
import fasttext
import fasttext.util
import umap
import hdbscan
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Load medical records (replace this with loading your dataset)
medical_records = [
    "Patient shows signs of pneumonia.",
    "Diagnosed with type 2 diabetes.",
    "Symptoms include coughing and high fever.",
    "High blood sugar levels detected.",
    "Chest X-ray confirms pneumonia.",
    "Requires insulin for diabetes.",
]

# 1. Data Preprocessing
def preprocess_text(text):
    # Basic preprocessing: lowercasing and removing special characters
    return ''.join(e for e in text if (e.isalnum() or e.isspace()))

processed_records = [preprocess_text(record) for record in medical_records]

# 2. Vectorization using FastText Word Embeddings
fasttext.util.download_model('en', if_exists='ignore')  # English
ft_model = fasttext.load_model('cc.en.300.bin')
vectorized_records = np.array([ft_model.get_sentence_vector(record) for record in processed_records])

# 3. Dimensionality Reduction using UMAP
reducer = umap.UMAP(n_neighbors=5, min_dist=0.3)
embedding = reducer.fit_transform(vectorized_records)

# 4. Clustering using HDBSCAN
clusterer = hdbscan.HDBSCAN(min_samples=2, min_cluster_size=3)
clusters = clusterer.fit_predict(embedding)

# 5. Visualization using Plotly
df = pd.DataFrame(embedding, columns=['x', 'y'])
df['cluster'] = clusters
fig = px.scatter(df, x='x', y='y', color='cluster', hover_data=[df.index], width=800, height=600)
fig.show()

# 6. Saving & Loading Model (Optional)
# Save: ft_model.save_model("model_filename.bin")
# Load: loaded_model = fasttext.load_model("model_filename.bin")

if __name__ == "__main__":
    print(clusters)
