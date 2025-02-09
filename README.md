# Multi-Instance Snake Game with Reinforcement Learning

## Overview

This project implements a multi-instance Snake game using Pygame, enhanced with a reinforcement learning agent built using PyTorch. It allows multiple independent Snake games to run simultaneously on a grid while offering a simple UI for interaction and training.

## Features

- **Multiple Game Instances**: Run multiple Snake games on a grid layout.
- **Reinforcement Learning Agent**: A deep Q-learning model trains the Snake to optimize its gameplay.
- **Interactive UI**: Start, pause, and switch between training and inference modes using a control panel.
- **Model Training & Saving**: Train the agent across multiple episodes and save/load models seamlessly.
- **Adjustable Step Delay**: Modify game speed for better visualization or faster training.

### Prerequisites

Ensure you have Python installed (Python 3.7+ recommended). Install the required dependencies using:

```bash
pip install -r requirements.txt
```

### Dependencies

The project relies on the following libraries:

- `pygame` - For game rendering and user interaction.
- `torch` - For deep reinforcement learning.
- `numpy` - For numerical computations.

## Running the Project

You can start the multi-instance Snake game using:

```bash
python main.py
```

On Windows, you can also use the batch script:

```bash
run.bat
```

On macOS/Linux:

```bash
./run.sh
```

## Usage

1. **Start/Pause**: Use the control panel to start or pause all games.
2. **Training Mode**: The Snake agent learns through reinforcement learning.
3. **Inference Mode**: Load a pre-trained model to see the AI play.
4. **Modify Game Speed**: Adjust step delay in the control panel.
5. **Add/Remove Instances**: Click on grid cells to start or remove game instances.

## Saving and Loading Models

To save the trained model:

```bash
python save_model.py --output model.pth
```

To load a model during inference:

1. Switch to inference mode.
2. Click the load button on a game instance.
3. Select the saved `.pth` model file.

## Project Structure

```
project/
├── README.md
├── requirements.txt
├── config.py
├── main.py
├── agent/
│   ├── __init__.py
│   ├── snake_net.py
│   └── snake_agent.py
├── game/
│   ├── __init__.py
│   └── snake_game.py
├── ui/
│   ├── __init__.py
│   └── control_panel.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── models/                 # Folder for saved model checkpoints
├── setup.bat               # Windows setup script
├── run.bat                 # Windows run script
├── setup.sh                # Bash setup script
└── run.sh                  # Bash run script
```

## Future Improvements

- Implementing a more advanced neural network for better performance.
- Introducing additional game mechanics for richer training.
- Optimizing training efficiency through experience replay.

## License

This project is licensed under the MIT License. Feel free to modify and distribute.
