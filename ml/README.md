# INCLUSIFY Data Collection and Weak Labeling Pipeline

This pipeline collects academic English text from PDFs, extracts sentences, generates semantic embeddings, performs unsupervised clustering, and outputs weakly-labeled training data for LoRA fine-tuning.

## Overview

The pipeline consists of modular components:

- **PDF Scraping**: Discovers and downloads PDF files from a target URL
- **Text Extraction**: Extracts and cleans text from PDF files
- **Sentence Splitting**: Splits text into sentences with filtering
- **Embedding Generation**: Generates semantic embeddings using sentence transformers
- **Clustering**: Performs HDBSCAN clustering to create weak labels

## Setup

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Navigate to the `ml` directory:
```bash
cd ml
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. The pipeline will automatically download NLTK data on first run.

## Usage

### Basic Usage

Run the pipeline with a target URL:

```bash
python pipeline.py https://example.com/academic-papers
```

Or modify the `TARGET_URL` variable in `pipeline.py` and run:

```bash
python pipeline.py
```

### Pipeline Steps

The pipeline executes the following steps:

1. **PDF Scraping**: Crawls the target URL and downloads all linked PDF files to `data/raw_pdfs/`
2. **Text Extraction**: Extracts and cleans text from each PDF (removes headers, footers, references)
3. **Sentence Splitting**: Splits text into sentences, filters for English and minimum length
4. **Raw Dataset Creation**: Creates `data/output/sentences_raw.csv`
5. **Embedding Generation**: Generates semantic embeddings using `all-mpnet-base-v2`
6. **Clustering**: Performs HDBSCAN clustering to assign weak labels
7. **Labeled Dataset Creation**: Creates `data/output/sentences_clustered.csv`

### Output Files

#### `sentences_raw.csv`

Contains all extracted sentences with metadata:

```csv
sentence_id,sentence_text,source_pdf,source_url
1,"This is a sample sentence.",paper1.pdf,https://example.com/paper1.pdf
2,"Another sentence here.",paper1.pdf,https://example.com/paper1.pdf
```

#### `sentences_clustered.csv`

Contains sentences with cluster-based weak labels:

```csv
sentence_id,sentence_text,cluster_id,source_pdf,source_url
1,"This is a sample sentence.",0,paper1.pdf,https://example.com/paper1.pdf
2,"Another sentence here.",1,paper1.pdf,https://example.com/paper1.pdf
```

**Note**: `cluster_id = -1` indicates noise points (outliers) that don't belong to any cluster.

## Configuration

### Pipeline Parameters

You can modify parameters in `pipeline.py`:

- `target_url`: URL to scrape for PDFs
- `min_tokens`: Minimum tokens per sentence (default: 5)
- `min_cluster_size`: Minimum cluster size for HDBSCAN (default: 10)
- `min_samples`: Minimum samples for HDBSCAN (default: 5)
- `metric`: Distance metric for clustering (default: 'euclidean')

### Model Configuration

The embedding model can be changed in `embeddings/encoder.py`:

- Default: `sentence-transformers/all-mpnet-base-v2`
- Alternative: `sentence-transformers/all-MiniLM-L6-v2` (faster, smaller)

## Module Structure

```
ml/
├── data/
│   ├── raw_pdfs/           # Downloaded PDFs
│   └── output/             # Output CSV files
├── data_collection/
│   ├── pdf_scraper.py      # PDF discovery and download
│   └── text_extractor.py   # Text extraction and cleaning
├── preprocessing/
│   └── sentence_splitter.py # Sentence splitting and filtering
├── embeddings/
│   └── encoder.py          # Sentence embedding generation
├── clustering/
│   └── clusterer.py         # HDBSCAN clustering
├── pipeline.py              # Main orchestration script
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Error Handling

The pipeline handles:

- Network errors during PDF download (logs and continues)
- Corrupted/unreadable PDFs (skips with warning)
- Empty text extraction (skips PDF)
- Invalid sentences (filters out)

All errors are logged with appropriate detail levels.

## Future Extensibility

The pipeline is designed to be extended for:

- **Hebrew support**: Add language detection and Hebrew tokenizer
- **Configurable URLs**: Move from hardcoded to config file
- **Embedding persistence**: Option to save embeddings for reuse
- **Multiple clustering algorithms**: Support for KMeans, Agglomerative, etc.

## Troubleshooting

### NLTK Data Download Issues

If NLTK data fails to download automatically:

```python
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
```

### Memory Issues

For large datasets, consider:

- Reducing batch size in `embeddings/encoder.py`
- Processing PDFs in smaller batches
- Using a smaller embedding model

### Clustering Issues

If too many noise points are generated:

- Reduce `min_cluster_size` and `min_samples`
- Try `metric='cosine'` instead of `euclidean`
- Check embedding quality

## License

Part of the INCLUSIFY project.
