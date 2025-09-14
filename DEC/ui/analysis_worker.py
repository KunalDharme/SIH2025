# analysis_worker.py
from PyQt5.QtCore import QThread, pyqtSignal
import os
import time
import datetime
import pandas as pd
import shutil
from pathlib import Path
from typing import List, Dict, Any, Set

from dec.scanner import scan_directory
from dec.categorizer import categorize_file
from dec.keyword_search import load_keywords, search_keywords
from dec.scoring import assign_risk_level


class AnalysisWorker(QThread):
    """
    Worker thread to perform file scanning, categorization,
    keyword searching, and risk scoring asynchronously.
    Updated to handle configuration from setup wizard.
    """
    progress_update = pyqtSignal(int)       # Percent progress (0-100)
    log_update = pyqtSignal(str)            # Log messages
    task_update = pyqtSignal(str)           # Current task description
    stats_update = pyqtSignal(dict)         # Statistics updates
    finished_signal = pyqtSignal(object)    # Final pandas DataFrame
    error_signal = pyqtSignal(str)          # Error messages

    def __init__(self, analysis_config: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.config = analysis_config
        self.source = Path(analysis_config["source_folder"])
        self.dest = Path(analysis_config["dest_folder"])
        self.should_stop = False
        
        # Analysis statistics
        self.files_processed = 0
        self.suspicious_files = 0
        self.copied_files = 0

    def stop(self):
        """Request the worker to stop processing"""
        self.should_stop = True

    def run(self):
        """Main analysis execution"""
        try:
            self.should_stop = False
            self._run_analysis()
        except Exception as e:
            self.error_signal.emit(f"Critical error during analysis: {str(e)}")
            self.finished_signal.emit(None)

    def _run_analysis(self):
        """Execute the complete analysis workflow"""
        # Validate and prepare
        if not self._validate_configuration():
            return

        if not self._prepare_destination():
            return

        # Load keywords based on configuration
        keywords = self._load_keywords()
        if keywords is None:
            return

        # Scan and filter files
        files = self._scan_and_filter_files()
        if not files:
            return

        # Process files
        results = self._process_files(files, keywords)
        if results is None:
            return

        # Finalize and return results
        self._finalize_analysis(results)

    def _validate_configuration(self) -> bool:
        """Validate the analysis configuration"""
        self.task_update.emit("Validating configuration...")
        
        if not self.source.exists():
            self.error_signal.emit(f"Source directory does not exist: {self.source}")
            return False

        if not self.source.is_dir():
            self.error_signal.emit(f"Source path is not a directory: {self.source}")
            return False

        self.log_update.emit(f"Configuration validated successfully")
        return True

    def _prepare_destination(self) -> bool:
        """Prepare the destination directory"""
        self.task_update.emit("Preparing destination directory...")
        
        try:
            # Create destination directory if it doesn't exist
            self.dest.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories if copying suspicious files
            if self.config.get("copy_suspicious", False):
                suspicious_dir = self.dest / "suspicious_files"
                suspicious_dir.mkdir(exist_ok=True)
                self.log_update.emit(f"Created suspicious files directory: {suspicious_dir}")
            
            self.log_update.emit(f"Destination prepared: {self.dest}")
            return True
            
        except Exception as e:
            self.error_signal.emit(f"Failed to prepare destination: {str(e)}")
            return False

    def _load_keywords(self) -> List[str]:
        """Load keywords based on configuration"""
        self.task_update.emit("Loading keyword database...")
        
        try:
            if self.config.get("use_custom_keywords", False):
                custom_file = self.config.get("custom_keyword_file")
                if custom_file and os.path.exists(custom_file):
                    keywords = self._load_custom_keywords(custom_file)
                    self.log_update.emit(f"Loaded {len(keywords)} custom keywords from {os.path.basename(custom_file)}")
                else:
                    self.log_update.emit("Custom keyword file not found, falling back to built-in keywords")
                    keywords = load_keywords()
            else:
                keywords = load_keywords()
                self.log_update.emit(f"Loaded {len(keywords)} built-in security keywords")
            
            return keywords
            
        except Exception as e:
            self.error_signal.emit(f"Failed to load keywords: {str(e)}")
            return None

    def _load_custom_keywords(self, file_path: str) -> List[str]:
        """Load keywords from custom file"""
        keywords = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    keyword = line.strip()
                    if keyword and not keyword.startswith('#'):  # Skip empty lines and comments
                        keywords.append(keyword)
            return keywords
        except Exception as e:
            self.log_update.emit(f"Error reading custom keyword file: {str(e)}")
            return load_keywords()  # Fallback to built-in

    def _scan_and_filter_files(self) -> List[Dict[str, Any]]:
        """Scan directory and filter files based on configuration"""
        self.task_update.emit("Scanning directory structure...")
        
        try:
            # Get all files
            all_files = list(scan_directory(self.source))
            self.log_update.emit(f"Found {len(all_files)} total files")
            
            if self.should_stop:
                return []
            
            # Filter by file extensions if specified
            selected_extensions = self.config.get("selected_extensions", [])
            if selected_extensions:
                filtered_files = []
                for file_info in all_files:
                    file_path = Path(file_info.get("path", ""))
                    file_ext = file_path.suffix.lower()
                    
                    if file_ext in selected_extensions:
                        filtered_files.append(file_info)
                
                self.log_update.emit(f"Filtered to {len(filtered_files)} files matching selected types")
                return filtered_files
            else:
                self.log_update.emit("No file type filtering applied - analyzing all files")
                return all_files
                
        except Exception as e:
            self.error_signal.emit(f"Failed to scan directory: {str(e)}")
            return []

    def _process_files(self, files: List[Dict[str, Any]], keywords: List[str]) -> List[Dict[str, Any]]:
        """Process each file according to security level and configuration"""
        if not files:
            self.log_update.emit("No files to process")
            return []

        self.task_update.emit("Processing files...")
        total = len(files)
        results = []
        security_level = self.config.get("security_level", "Standard Scan")
        
        self.log_update.emit(f"Starting {security_level.lower()} of {total} files...")
        
        # Determine processing intensity based on security level
        if security_level == "Quick Scan":
            process_intensity = 1  # Basic checks only
        elif security_level == "Deep Scan":
            process_intensity = 3  # Comprehensive analysis
        else:  # Standard Scan
            process_intensity = 2  # Balanced approach

        for idx, file_info in enumerate(files, start=1):
            if self.should_stop:
                self.log_update.emit("Processing stopped by user")
                break

            try:
                result = self._process_single_file(file_info, keywords, process_intensity)
                if result:
                    results.append(result)
                    
                    # Update statistics
                    self.files_processed += 1
                    if result.get("risk_level", "").lower() in ["high", "critical"]:
                        self.suspicious_files += 1
                        
                        # Copy suspicious file if configured
                        if self.config.get("copy_suspicious", False):
                            self._copy_suspicious_file(result["path"])
                    
                    # Update progress and statistics
                    progress = int((idx / total) * 100)
                    self.progress_update.emit(progress)
                    self.stats_update.emit({
                        "files_processed": self.files_processed,
                        "suspicious_found": self.suspicious_files
                    })
                
                # Log progress periodically
                if idx % 50 == 0 or idx == total:
                    self.log_update.emit(f"Processed {idx}/{total} files ({progress}%)")

            except Exception as e:
                file_path = file_info.get("path", "unknown")
                self.log_update.emit(f"Error processing {file_path}: {str(e)}")
                continue

            # Small delay for UI responsiveness
            time.sleep(0.005)

        return results

    def _process_single_file(self, file_info: Dict[str, Any], keywords: List[str], intensity: int) -> Dict[str, Any]:
        """Process a single file with specified intensity level"""
        # Handle different file_info structures safely
        if isinstance(file_info, dict):
            file_path = Path(file_info.get("path", ""))
        else:
            file_path = Path(str(file_info))
        
        if not file_path.exists():
            return None

        try:
            # Basic file metadata
            stat_info = file_path.stat()
            size = stat_info.st_size
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Debug: Try categorize_file
            try:
                category = categorize_file(str(file_path))  # Convert to string
            except Exception as e:
                self.log_update.emit(f"Error in categorize_file for {file_path.name}: {str(e)}")
                category = "Unknown"
            
            # Debug: Try keyword search based on intensity
            try:
                if intensity == 1:  # Quick scan - filename only
                    kw_hits = search_keywords(str(file_path.name), keywords)
                elif intensity == 3:  # Deep scan - comprehensive
                    kw_hits = self._deep_keyword_search(file_path, keywords)
                else:  # Standard scan - balanced
                    kw_hits = search_keywords(str(file_path), keywords)
                
                # Ensure kw_hits is a list
                if not isinstance(kw_hits, list):
                    kw_hits = []
                    
            except Exception as e:
                self.log_update.emit(f"Error in keyword search for {file_path.name}: {str(e)}")
                kw_hits = []
            
            keywords_found = ",".join(kw_hits) if kw_hits else ""
            
            # Debug: Try risk assignment
            try:
                risk = assign_risk_level(keywords_found)
            except Exception as e:
                self.log_update.emit(f"Error in risk assignment for {file_path.name}: {str(e)}")
                risk = "Low"
            
            # Build result record
            result = {
                "path": str(file_path),
                "filename": file_path.name,
                "size": size,
                "category": category,
                "keywords": keywords_found,
                "keyword_count": len(kw_hits),
                "risk_level": risk,
                "timestamp": timestamp,
                "analysis_level": self.config.get("security_level", "Standard"),
            }
            
            return result
            
        except Exception as e:
            self.log_update.emit(f"Failed to process {file_path.name}: {str(e)}")
            return None

    def _deep_keyword_search(self, file_path: Path, keywords: List[str]) -> List[str]:
        """Perform deep keyword search for comprehensive analysis"""
        hits = []
        
        # Search in filename
        hits.extend(search_keywords(str(file_path.name), keywords))
        
        # Search in full path
        hits.extend(search_keywords(str(file_path), keywords))
        
        # For text files, search content (limited to avoid performance issues)
        if file_path.suffix.lower() in ['.txt', '.log', '.csv', '.json', '.xml', '.html']:
            try:
                if file_path.stat().st_size < 10 * 1024 * 1024:  # Less than 10MB
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(50000)  # Read first 50KB only
                        hits.extend(search_keywords(content, keywords))
            except:
                pass  # Skip content search if file can't be read
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(hits))

    def _copy_suspicious_file(self, file_path: str):
        """Copy suspicious file to destination if configured"""
        try:
            source_file = Path(file_path)
            if not source_file.exists():
                return
                
            suspicious_dir = self.dest / "suspicious_files"
            dest_file = suspicious_dir / source_file.name
            
            # Handle filename conflicts
            counter = 1
            while dest_file.exists():
                name_parts = source_file.stem, counter, source_file.suffix
                dest_file = suspicious_dir / f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                counter += 1
            
            shutil.copy2(source_file, dest_file)
            self.copied_files += 1
            self.log_update.emit(f"Copied suspicious file: {source_file.name}")
            
        except Exception as e:
            self.log_update.emit(f"Failed to copy suspicious file {file_path}: {str(e)}")

    def _finalize_analysis(self, results: List[Dict[str, Any]]):
        """Finalize analysis and emit results"""
        if not results:
            self.log_update.emit("Analysis completed with no results")
            self.finished_signal.emit(pd.DataFrame())
            return

        try:
            # Create DataFrame
            df = pd.DataFrame(results)
            
            # Add summary statistics
            total_files = len(df)
            high_risk = len(df[df['risk_level'].isin(['High', 'Critical'])])
            
            self.task_update.emit("Analysis completed successfully")
            self.log_update.emit(f"Analysis Summary:")
            self.log_update.emit(f"- Total files analyzed: {total_files}")
            self.log_update.emit(f"- High/Critical risk files: {high_risk}")
            self.log_update.emit(f"- Files copied: {self.copied_files}")
            
            # Save results to CSV
            try:
                results_file = self.dest / f"analysis_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(results_file, index=False)
                self.log_update.emit(f"Results saved to: {results_file}")
            except Exception as e:
                self.log_update.emit(f"Warning: Could not save CSV file: {str(e)}")
            
            self.finished_signal.emit(df)
            
        except Exception as e:
            self.error_signal.emit(f"Failed to finalize results: {str(e)}")
            self.finished_signal.emit(None)