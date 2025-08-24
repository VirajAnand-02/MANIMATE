"""
Test script to demonstrate parallel processing performance improvements
"""

import time
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.parallel import (
    ParallelProcessor, ParallelConfig, TTSParallelProcessor, 
    parallel_decorator, parallel_file_operations
)
from src.providers.tts import create_tts_provider
from src.core.models import TTSConfig, TTSProvider
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_parallel_vs_sequential():
    """Test parallel vs sequential processing performance"""
    
    print("🧪 Testing Parallel vs Sequential Processing Performance")
    print("=" * 60)
    
    # Create mock TTS provider for testing
    tts_config = TTSConfig(provider=TTSProvider.MOCK, voice="Aoede")
    tts_provider = create_tts_provider("mock", **tts_config.dict())
    
    # Test data
    test_texts = [
        "Introduction to linear algebra and matrix operations",
        "Understanding eigenvalues and eigenvectors in mathematics",
        "Applications of calculus in machine learning algorithms",
        "Probability theory and statistical inference fundamentals",
        "Differential equations and their real-world applications",
        "Vector spaces and linear transformations explained",
        "Graph theory basics and algorithmic applications",
        "Number theory concepts in modern cryptography"
    ]
    
    test_requests = [
        (text, Path(f"temp_audio_{i}.wav"))
        for i, text in enumerate(test_texts)
    ]
    
    print(f"📝 Testing with {len(test_requests)} TTS requests")
    print()
    
    # Test 1: Sequential Processing
    print("🔄 Sequential Processing Test")
    start_time = time.time()
    
    sequential_results = {}
    for i, (text, output_path) in enumerate(test_requests):
        success = tts_provider.synthesize(text, output_path)
        sequential_results[f"seq_{i}"] = success
    
    sequential_time = time.time() - start_time
    sequential_success = sum(1 for success in sequential_results.values() if success)
    
    print(f"✅ Sequential completed: {sequential_success}/{len(test_requests)} in {sequential_time:.2f}s")
    print()
    
    # Test 2: Parallel Processing (Base class method)
    print("⚡ Parallel Processing Test (Base Method)")
    start_time = time.time()
    
    parallel_results = tts_provider.synthesize_batch(test_requests, max_workers=4)
    
    parallel_time = time.time() - start_time
    parallel_success = sum(1 for success in parallel_results.values() if success)
    
    print(f"✅ Parallel completed: {parallel_success}/{len(test_requests)} in {parallel_time:.2f}s")
    print()
    
    # Test 3: TTSParallelProcessor
    print("🚀 TTSParallelProcessor Test")
    start_time = time.time()
    
    tts_parallel = TTSParallelProcessor(tts_provider, max_workers=4)
    
    # Convert to expected format
    parallel_requests = [
        {"scene": type('Scene', (), {'text': text, 'seq': i}), "audio_file": output_path}
        for i, (text, output_path) in enumerate(test_requests)
    ]
    
    processor_results = tts_parallel.synthesize_batch(parallel_requests)
    
    processor_time = time.time() - start_time
    processor_success = len(processor_results)
    
    print(f"✅ TTSParallelProcessor completed: {processor_success}/{len(test_requests)} in {processor_time:.2f}s")
    print()
    
    # Performance Summary
    print("📊 Performance Summary")
    print("-" * 40)
    print(f"Sequential:           {sequential_time:.2f}s")
    print(f"Parallel (Base):      {parallel_time:.2f}s")
    print(f"TTSParallelProcessor: {processor_time:.2f}s")
    print()
    
    if sequential_time > 0:
        base_speedup = sequential_time / parallel_time if parallel_time > 0 else 0
        processor_speedup = sequential_time / processor_time if processor_time > 0 else 0
        
        print(f"🏆 Speedup - Base Method: {base_speedup:.2f}x")
        print(f"🏆 Speedup - TTSProcessor: {processor_speedup:.2f}x")
    
    print()


def test_parallel_decorator():
    """Test the parallel decorator functionality"""
    
    print("🎯 Testing Parallel Decorator")
    print("=" * 40)
    
    # Define a simple test function
    def process_number(n):
        """Simulate some processing work"""
        time.sleep(0.1)  # Simulate work
        return n * n
    
    # Test data
    numbers = list(range(1, 9))  # 1-8
    
    print(f"📝 Processing {len(numbers)} numbers: {numbers}")
    
    # Sequential test
    print("🔄 Sequential processing...")
    start_time = time.time()
    sequential_results = [process_number(n) for n in numbers]
    sequential_time = time.time() - start_time
    
    print(f"✅ Sequential results: {sequential_results}")
    print(f"⏱️  Sequential time: {sequential_time:.2f}s")
    print()
    
    # Parallel test with decorator
    print("⚡ Parallel processing with decorator...")
    
    @parallel_decorator(ParallelConfig(max_workers=4, use_threading=True))
    def parallel_process_numbers(numbers_list):
        pass  # The decorator handles the parallel processing
    
    start_time = time.time()
    parallel_results = parallel_process_numbers(numbers)
    parallel_time = time.time() - start_time
    
    print(f"✅ Parallel results: {parallel_results}")
    print(f"⏱️  Parallel time: {parallel_time:.2f}s")
    
    if sequential_time > 0 and parallel_time > 0:
        speedup = sequential_time / parallel_time
        print(f"🏆 Decorator speedup: {speedup:.2f}x")
    
    print()


def test_file_operations():
    """Test parallel file operations"""
    
    print("📁 Testing Parallel File Operations")
    print("=" * 40)
    
    import tempfile
    import os
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Define file operations
        operations = []
        
        for i in range(5):
            file_path = temp_path / f"test_file_{i}.txt"
            content = f"This is test file {i} with some content to write."
            
            def write_file(path, content):
                with open(path, 'w') as f:
                    f.write(content)
                return True
            
            operations.append((
                f"write_file_{i}",
                write_file,
                (file_path, content),
                {}
            ))
        
        print(f"📝 Creating {len(operations)} files in parallel...")
        
        # Execute file operations in parallel
        start_time = time.time()
        results = parallel_file_operations(operations, max_workers=3)
        parallel_time = time.time() - start_time
        
        successful = sum(1 for success in results.values() if success)
        
        print(f"✅ Created {successful}/{len(operations)} files in {parallel_time:.2f}s")
        
        # Verify files were created
        created_files = list(temp_path.glob("*.txt"))
        print(f"🔍 Verified {len(created_files)} files exist")
    
    print()


def main():
    """Run all parallel processing tests"""
    
    print("🚀 Parallel Processing Performance Tests")
    print("=" * 60)
    print()
    
    try:
        # Test 1: TTS Parallel vs Sequential
        test_parallel_vs_sequential()
        
        # Test 2: Parallel Decorator
        test_parallel_decorator()
        
        # Test 3: File Operations
        test_file_operations()
        
        print("🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
