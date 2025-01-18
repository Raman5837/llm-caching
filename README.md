# LLM Caching System

## Overview

This project implements a caching mechanism prototype for LLMs responses.
It optimizes response times and reduces redundant calls by caching query-response pairs along with any associated media files.
The design supports scalability and modularity, enabling easy extensions for future enhancements.

## Key Features

1. **Transformer Integration**

   - Uses `SentenceTransformer` to convert textual queries into dense vector embeddings.

2. **VectorDB Integration**

   - Uses a vector database (Qdrant) to store embeddings of user queries.
   - Efficiently retrieves cached responses for similar queries using cosine similarity.
   - Ensures response accuracy by incorporating a similarity threshold during searches.

3. **Media Storage**

   - Manages the storage and retrieval of media files (e.g., images) uploaded with user queries.
   - Currently, files are stored in a local directory on disk.
   - Designed to support extensions for cloud-based storage solutions like Amazon S3, Google Cloud Storage, or other bucket services.

4. **Cache Layer**
   - Provides a unified interface for interacting with the VectorDB and Media Storage.
   - Stores query-response pairs and associates media files (if provided) using metadata.
   - Handles expiration of cached entries based on a configurable TTL (Time-to-Live).

## Design Architecture

```
+--------------------+      +-----------------------+      +---------------------+
|   ChatInterface    |----->|   InteractionLayer    |----->|      CacheLayer     |
| (Client Interface) |      |       (For LLM)       |      |  (Text Transformer) |
|                    |      |                       |      |                     |
|                    |      |                       |      |                     |
+--------------------+      +-----------------------+      +---------------------+
         |                                                           |
         |                                                           |
+---------------------+                                    +---------------------+
|  ImageProcessor     |                                    |      Vector DB      |
| (Handles OCR for    |                                    | (Query, Embedding,  |
|    Images)          |                                    |  Metadata, Cosine)  |
+---------------------+                                    +---------------------+
                                                               |
                                                               |
                                       +-----------------------+----------------------+
                                       |                                              |
                                       |                                              |
                           +---------------------+                          +----------------------+
                           |     Media Storage   |                          |  Local File System   |
                           | (Handles Media Files|                          | (Stores Media Files) |
                           |   for Queries)      |                          |                      |
                           +---------------------+                          +----------------------+

```

## Components

1. **Cache Layer**

   - Acts as the central interface for caching and retrieving responses.
   - Combines query embeddings and media file metadata to store or retrieve cached entries.
   - Automatically deletes expired entries based on the TTL configuration.

2. **VectorDB**

   - Handles storage of query embeddings and metadata.
   - Efficient similarity-based searches for cached responses.
   - Uses Qdrant as the vector database with cosine distance for similarity.

3. **Media Storage**

   - Handles uploading, retrieving, and deleting media files associated with queries.
   - Currently stores files in a local directory.
   - Extendable to support cloud providers like Amazon S3 or Google Cloud Storage.

4. **Image Processor (OCR)**

   - Analyzes image content using OCR to extract relevant text and coordinates of specific elements (like buttons, fields).
   - Uses labels or identifiers in the image (e.g., a button labeled "Submit") to pinpoint exact coordinates or regions.
   - These coordinates are then used to map and trigger corresponding actions in the InteractionLayer.

5. **Text Transformer (Sentence Transformer)**

   - Converts textual content (queries or extracted OCR text) into vector representations.
   - Uses Sentence Transformers to create embeddings that capture semantic meaning.
   - Embeddings are stored in the VectorDB for similarity-based search and retrieval.

## Installation

    Clone the repository
    cd llm-caching
    Run `python -m pip install -r requirements.txt` to install the dependencies.
    Run `python main.py` to execute the code.
