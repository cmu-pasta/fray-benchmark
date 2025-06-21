# Container Usage Guide

This document explains how to build and use the fray-benchmark container created with nix2container.

## Building the Container

To build the container image:

```bash
nix build .#container
```

This will create a container image that includes:
- All source code from the workspace
- Python environment with all dependencies from pyproject.toml
- Java development environment (JDK 11 and JDK 21)
- Build tools (Maven, CMake, etc.)
- All system dependencies from the dev shell

## Loading the Container

After building, load the container into Docker:

```bash
docker load < result
```

## Running the Container

### Interactive Mode

To start an interactive shell in the container:

```bash
docker run -it --rm fray-benchmark:latest
```

This will:
1. Set up the environment (Java paths, Python virtual environment)
2. Show workspace contents
3. Display version information
4. Start an interactive bash shell

### Running Commands

To run specific commands in the container:

```bash
docker run -it --rm fray-benchmark:latest python -m fray_benchmark --help
```

### With Volume Mounts

To persist output and access local files:

```bash
docker run -it --rm \
  -v "$(pwd)/output:/workspace/output" \
  -v "$(pwd)/local-data:/workspace/local-data" \
  fray-benchmark:latest
```

## Container Structure

The container includes:
- `/workspace` - Complete source code from the fray-benchmark repository
- Python virtual environment automatically set up with uv
- All Java dependencies (JDK 11, JDK 21, Maven)
- All build tools and system dependencies
- Environment setup scripts

## Convenience Apps

You can also use the flake apps for easier container management:

```bash
# Build the container
nix run .#build-container

# Run the container with volume mounts
nix run .#run-container
```

## Environment Variables

The container sets up these key environment variables:
- `JDK11_HOME` - Path to JDK 11
- `JDK21_HOME` - Path to JDK 21 
- `JAVA_HOME` - Points to JDK 21 (default)
- `VIRTUAL_ENV` - Python virtual environment path
- `PYTHONPATH` - Set to `/workspace`

## Troubleshooting

If you encounter issues:
1. Check that all dependencies are properly installed in the virtual environment
2. Verify Java versions are accessible
3. Ensure workspace files are properly copied to `/workspace`
4. Check that scripts have executable permissions

The setup script provides detailed output about the environment setup process.
