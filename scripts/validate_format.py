import os
import sys
import yaml
from glob import glob

# Define the allowed technologies
ALLOWED_TECHNOLOGIES = {
    # Programming languages
    "python", "java", "c", "c++", "c-sharp", "javascript", "typescript", "ruby",
    "php", "go", "rust", "kotlin", "swift", "scala", "perl", "dart",
    # Containerization and orchestration
    "docker", "podman", "kubernetes", "openshift", "docker-compose",
    "cri-o", "containerd", "helm", "rancher", "docker-swarm",
    # Cloud computing
    "aws", "azure", "gcp", "ibm-cloud", "oracle-cloud", "alibaba-cloud",
    "ec2", "s3", "rds", "eks", "lambda", "azure-vm", "azure-functions",
    "cloud-run", "firebase", "cloudflare",
    # Databases
    "postgresql", "mysql", "mariadb", "sql-server", "oracle-db",
    "mongodb", "cassandra", "dynamodb", "redis", "couchbase", "neo4j",
    "arangodb", "influxdb", "prometheus", "timescale",
    # DevOps and infrastructure
    "terraform", "ansible", "chef", "puppet", "packer", "vault", "consul",
    "jenkins", "gitlab-ci", "github-actions", "spinnaker", "argo-cd", "flux",
    # Security
    "nmap", "wireshark", "burp-suite", "metasploit", "nessus",
    "kali-linux", "trivy", "fail2ban",
    # Monitoring and observability
    "grafana", "datadog", "splunk", "new-relic", "elasticsearch", "kibana",
    "fluentd", "opentelemetry", "jaeger",
    # Web development
    "react", "angular", "vue", "svelte", "nextjs", "nuxtjs", "tailwindcss",
    "bootstrap", "material-ui", "express", "django", "flask", "fastapi",
    "spring", "laravel", "rails", "asp-net",
    # AI and machine learning
    "tensorflow", "pytorch", "keras", "scikit-learn", "numpy", "pandas",
    "opencv", "huggingface", "mlflow", "kubeflow",
    # Big data
    "hadoop", "spark", "kafka", "hive", "pig", "flink", "presto", "dremio",
    # Operating systems
    "linux", "windows", "macos", "ubuntu", "centos", "debian", "fedora",
    "redhat", "alpine",
    # Versioning and collaboration tools
    "git", "github", "gitlab", "bitbucket", "mercurial", "svn", "jira",
    "trello", "confluence", "slack", "teams"
}

def validate_technologies(technologies):
    """Ensure technologies are in the allowed list."""
    invalid_technologies = [tech for tech in technologies if tech not in ALLOWED_TECHNOLOGIES]
    return invalid_technologies

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
                
                # Validate technologies
                if "technologies" in data:
                    invalid_technologies = validate_technologies(data["technologies"])
                    if invalid_technologies:
                        invalid_files.append(f"{file}: Invalid technologies - {', '.join(invalid_technologies)}")
            
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
