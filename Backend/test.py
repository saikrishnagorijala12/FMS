#!/usr/bin/env python3
"""
Script to traverse all files in a directory and copy their content
into a new file along with file locations.
"""

import os
import sys
from pathlib import Path


def aggregate_files(source_dir, output_file, file_extensions=None, max_file_size=10 * 1024 * 1024):
    """
    Aggregate content from all files in source_dir into output_file.

    Args:
        source_dir (str): Directory to traverse
        output_file (str): Output file path
        file_extensions (list): List of file extensions to include (e.g., ['.py', '.txt'])
                               If None, includes all files
        max_file_size (int): Maximum file size in bytes to process (default: 10MB)
    """

    source_path = Path(source_dir)

    if not source_path.exists():
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return

    if not source_path.is_dir():
        print(f"Error: '{source_dir}' is not a directory.")
        return

    # Create output directory if it doesn't exist
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    processed_files = 0
    skipped_files = 0

    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Write header
            outfile.write(f"File Content Aggregation\n")
            outfile.write(f"Source Directory: {source_path.absolute()}\n")
            outfile.write(f"Generated on: {__import__('datetime').datetime.now()}\n")
            outfile.write("=" * 80 + "\n\n")

            # Traverse all files
            for file_path in source_path.rglob('*'):
                if file_path.is_file():
                    # Skip the output file itself
                    if file_path.absolute() == output_path.absolute():
                        continue

                    # Filter by file extensions if specified
                    if file_extensions and file_path.suffix.lower() not in file_extensions:
                        continue

                    # Check file size
                    try:
                        file_size = file_path.stat().st_size
                        if file_size > max_file_size:
                            outfile.write(f"SKIPPED (too large: {file_size:,} bytes): {file_path}\n")
                            outfile.write("-" * 80 + "\n\n")
                            skipped_files += 1
                            continue
                    except OSError as e:
                        outfile.write(f"SKIPPED (error accessing): {file_path} - {e}\n")
                        outfile.write("-" * 80 + "\n\n")
                        skipped_files += 1
                        continue

                    # Write file header
                    outfile.write(f"FILE: {file_path}\n")
                    outfile.write(f"RELATIVE PATH: {file_path.relative_to(source_path)}\n")
                    outfile.write(f"SIZE: {file_size:,} bytes\n")
                    outfile.write("-" * 80 + "\n")

                    # Try to read and write file content
                    try:
                        # Try UTF-8 first
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                            outfile.write(content)
                    except UnicodeDecodeError:
                        try:
                            # Try with latin-1 encoding
                            with open(file_path, 'r', encoding='latin-1') as infile:
                                content = infile.read()
                                outfile.write(f"[Content decoded with latin-1 encoding]\n")
                                outfile.write(content)
                        except Exception as e:
                            # If still fails, treat as binary
                            outfile.write(f"[Binary file - content not displayed]\n")
                            outfile.write(f"Error: {e}\n")
                    except Exception as e:
                        outfile.write(f"[Error reading file: {e}]\n")
                        skipped_files += 1
                        continue

                    outfile.write("\n" + "=" * 80 + "\n\n")
                    processed_files += 1

                    # Progress indicator
                    if processed_files % 10 == 0:
                        print(f"Processed {processed_files} files...")

        print(f"Aggregation complete!")
        print(f"Processed files: {processed_files}")
        print(f"Skipped files: {skipped_files}")
        print(f"Output written to: {output_path.absolute()}")

    except Exception as e:
        print(f"Error creating output file: {e}")


def main():
    """Main function to handle command line arguments."""

    if len(sys.argv) < 2:
        print("Usage: python file_aggregator.py <source_directory> [output_file] [file_extensions]")
        print("\nExamples:")
        print("  python file_aggregator.py ./my_project")
        print("  python file_aggregator.py ./my_project output.txt")
        print("  python file_aggregator.py ./my_project output.txt .py,.js,.html")
        return

    source_dir = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "aggregated_files.txt"

    # Parse file extensions if provided
    file_extensions = None
    if len(sys.argv) > 3:
        extensions_str = sys.argv[3]
        file_extensions = [ext.strip() for ext in extensions_str.split(',')]
        if file_extensions:
            print(f"Filtering for extensions: {file_extensions}")

    print(f"Source directory: {source_dir}")
    print(f"Output file: {output_file}")
    print("Starting aggregation...")

    aggregate_files(source_dir, output_file, file_extensions)


if __name__ == "__main__":
    main()


# Alternative: Simple function for direct use
def simple_aggregate(directory, output="all_files_content.txt"):
    """
    Simple version - aggregates all text files from directory.

    Usage:
        simple_aggregate("./my_project", "output.txt")
    """
    aggregate_files(directory, output)


# Alternative: Only specific file types
def aggregate_code_files(directory, output="code_files.txt"):
    """
    Aggregates only common code files.

    Usage:
        aggregate_code_files("./my_project", "code_output.txt")
    """
    code_extensions = ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php', '.rb']
    aggregate_files(directory, output, code_extensions)