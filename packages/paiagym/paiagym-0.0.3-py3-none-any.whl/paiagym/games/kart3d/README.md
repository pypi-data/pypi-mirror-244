# PAIAGym Kart3D

A 3D Kart Game on the PAIA Platform.

## Installation

```
paiagym install kart3d
```

## Usage for Container

You can checkout the Dockerfile for the Docker container.

To build the Docker image:
```
docker build -t paiagym:kart3d . --no-cache
```

To push the Docker image:
```
docker build -t paiagym:kart3d . --no-cache
```

If you are using Linux server, run before starting the container (install and config X server with NVIDIA Driver):
```
sudo sh display.sh
```
display.sh can be found at [display.sh](https://github.com/PAIA-Playful-AI-Arena/paiagym/blob/master/display.sh).

To start the container:
```
docker run -it --rm --gpus all -v /tmp/.X11-unix:/tmp/.X11-unix paiagym:kart3d
```