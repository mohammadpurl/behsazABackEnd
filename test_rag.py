#!/usr/bin/env python3
"""
Simple test script for the RAG system
"""

import os
import sys

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))


def test_rag_system():
    """Test the RAG system"""
    try:
        print("Testing RAG system...")

        # Test document loading
        from services.document_service import load_and_split_documents

        print("✓ Document service imported successfully")

        # Test config
        from config import settings

        print(f"✓ Config loaded: DOCS_DIR = {settings.DOCS_DIR}")
        print(f"✓ VECTORSTORE_DIR = {settings.VECTORSTORE_DIR}")

        # Test if data directory exists
        if os.path.exists(settings.DOCS_DIR):
            print(f"✓ Data directory exists: {settings.DOCS_DIR}")
            pdf_files = [f for f in os.listdir(settings.DOCS_DIR) if f.endswith(".pdf")]
            print(f"✓ Found {len(pdf_files)} PDF files: {pdf_files}")
        else:
            print(f"✗ Data directory not found: {settings.DOCS_DIR}")
            return False

        # Test document loading
        try:
            docs = load_and_split_documents()
            print(f"✓ Documents loaded and split: {len(docs)} chunks")
        except Exception as e:
            print(f"✗ Error loading documents: {e}")
            return False

        print("\n🎉 RAG system test passed!")
        return True

    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_rag_system()
    sys.exit(0 if success else 1)
