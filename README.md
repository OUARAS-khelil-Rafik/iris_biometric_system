# Iris Biometric System

This project aims to develop a biometric system for individual identification using iris recognition. The system allows users to input an iris image through a graphical interface and display the identity of the identified person from the database after processing steps.

## Features
- Extracts iris images from the Iris Database (upol.cz), consisting of 3 x 128 iris images (i.e., 3 x 64 left and 3 x 64 right).
- Utilizes the Scale Invariant Feature Transform (SIFT) method for feature extraction.
- Matches iris images using Euclidean distance.
- Provides a graphical user interface for user interaction.

## Installation

### Prerequisites
- Python 3.x installed
- Pip package manager installed

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/iris_biometric_system.git
