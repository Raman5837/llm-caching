# LLM Caching System

## Overview

The LLM Caching System is a prototype designed to optimize the interaction with Large Language Models (LLMs) by implementing an efficient caching mechanism. It reduces redundant LLM calls, optimizes response times, and provides a scalable and modular structure for future enhancements. The system supports both text-based and image-based queries, leveraging vector databases and multiple LLMs in a layered architecture.

## Design Architecture

```plaintext
+--------------------+
|   ChatInterface    |  <--- Main Abstraction Layer
| (Client Interface) |  Handles user queries and routes them to Interaction Layer
+--------------------+
          |
+-----------------------+
|   Interaction Layer   |  <--- Core Service Layer
|  (Orchestrates Logic) |  Manages LLMs, caching, processors, and utilities
+-----------------------+
          |
+----------------------+----------------------+----------------------+-----------------------+
|    ModelManager      |      Cache Layer     |      MediaStorage     |      BoxUtility      |
|   (Manages LLMs)     |  (Uses VectorDB for  | (Manages media files) |  (Bounding box ops)  |
|                      |  embeddings & cache) |                       |                      |
+----------------------+----------------------+-----------------------+-----------------------+
          |                                |                                        |
+-------------------+          +-----------------------+                    +-----------------------+
|    LLM Models     |          |     VectorDB         |                     |    ImageProcessor     |
| (Clip, MoonDream, |          |  (Embeddings &       |                     | (OCR, overlays, etc.) |
|  Ollama, etc.)    |          |   metadata store)    |                     +-----------------------+
+-------------------+          +-----------------------+
          |
+-----------------------+
|    TextProcessor      |  <--- Performs text embeddings, parses user prompts
+-----------------------+


```

---

## **Features**

1. **LLM Integration**

   - Supports multiple LLMs (`MoonDream`, `Ollama`, and `Clip`) that can work sequentially or independently based on the request.
   - Allows dynamic selection of models for specific use cases, such as object detection or natural language understanding.
   - Ensures modularity by abstracting LLM calls in the `InteractionLayer`.

2. **Text Embedding and Semantic Search**

   - Leverages `SentenceTransformer` for transforming textual queries into dense vector embeddings.
   - Uses embeddings for semantic similarity search, ensuring that similar queries retrieve cached responses.
   - Dynamically extracts identifiers (e.g., objects like "coconut", "flowers", "ice-cream", "man") from user prompts.

3. **Vector Database Integration**

   - Uses `Qdrant` as the vector database for storing and querying embeddings with cosine similarity.
   - Handles metadata storage for each query, such as file paths and response data.
   - Implements a configurable similarity threshold to ensure response accuracy.

4. **Media File Handling**

   - Manages storage and retrieval of media files (e.g., images) associated with user queries.
   - Currently utilizes a local file system but is extendable to cloud storage providers like Amazon S3, Google Cloud Storage, or Azure Blob Storage.

5. **Cache Layer**

   - Combines embeddings and metadata for efficient caching of query-response pairs.
   - Automatically handles cache expiration using a Time-to-Live (TTL) configuration.
   - Avoids redundant LLM calls by leveraging the cached embeddings for similarity-based retrieval.

6. **Image Processing (OCR)**

   - Processes images to extract relevant text and coordinates using OCR.
   - Maps extracted elements (e.g., buttons, fields) to actionable regions based on identifiers.
   - Draws bounding boxes or overlays on images to visually represent detected elements.

7. **Scalable Architecture**
   - Designed to support additional LLMs or features with minimal changes to the codebase.
   - Modular and extensible, allowing the addition of new storage backends, caching mechanisms, or processing layers.

---

## Installation

    git clone git@github.com:Raman5837/llm-caching.git
    cd llm-caching

    Run `python -m pip install -r requirements.txt` to install the dependencies.
    Run `python main.py` to execute the code.

## **Configuration and Usage**

### **Moondream Configuration**

1. **Option 1: Download the Model File**

   - Visit [Moondream](https://docs.moondream.ai/quick-start) to Download the required model file
   - Set the absolute file path to the model as an environment variable

2. **Option 2: Use the API Key**
   - Sign up for an account on [Moondream API](https://console.moondream.ai/)
   - Generate an API key from your account's developer section.
   - Set the API key as an environment variable

### **Ollama Configuration**

1. **Download Ollama**:

   - Visit [Ollama Official Website](https://ollama.ai/) to download the application for your platform.
   - Install Ollama on your machine.

2. **Run Ollama Locally**:
   - After installation, start the Ollama service on your machine by running:
     ```bash
     ollama serve
     ```

### **CLIP Configuration**

- No additional setup is required for CLIP.
- Ensure all dependencies are installed by running
