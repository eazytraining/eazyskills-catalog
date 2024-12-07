import os
import sys
import yaml
from glob import glob

def validate_technologies(technologies):
    """Ensure technologies are lowercase and use hyphens."""
    for tech in technologies:
        if not tech.islower() or " " in tech:
            return False
    return True

def validate_file_format(directory, required_fields):
    """Validate YAML file content in a directory."""
    files = glob(f"{directory}/*.yaml")
    invalid_files = []

    for file in files:
        with open(file, "r") as f:
            try:
                data = yaml.safe_load(f)
                
                # Check required fields
                for field in required_fields:
                    if field not in data:
                        invalid_files.append(f"{file}: Missing field '{field}'")
                
                # Check technologies format
                if "technologies" in data and not validate_technologies(data["technologies"]):
                    invalid_files.append(f"{file}: Invalid technologies format.")
            
            except yaml.YAMLError as e:
                invalid_files.append(f"{file}: YAML parsing error - {e}")
    
    return invalid_files

if __name__ == "__main__":
    errors = []
    
    # Define required fields for each category
    required_fields_courses = ["name", "url", "duration_hours", "level", "objectives", "description", "technologies", "language", "deprecated"]
    required_fields_paths = ["name", "target_role", "course_ids", "language", "deprecated"]
    required_fields_bootcamps = ["name", "target_role", "modules", "duration_weeks", "language", "deprecated"]
    
    # Validate content for each category
    errors += validate_file_format("courses", required_fields_courses)
    errors += validate_file_format("paths", required_fields_paths)
    errors += validate_file_format("bootcamps", required_fields_bootcamps)
    
    if errors:
        print("Invalid file content detected:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("All file contents are valid.")
