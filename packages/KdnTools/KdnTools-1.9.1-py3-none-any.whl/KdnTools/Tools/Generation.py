from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
import numpy as np


class Generation:
    def __init__(self):
        """Initialize the Generator object."""
        pass

    @staticmethod
    def generate_2d_perlin_noise(width, height, scale, octaves, seed):
        """
        Generate 2D Perlin noise.

        Parameters:
        - width (int): The width of the noise grid.
        - height (int): The height of the noise grid.
        - scale (float): The scale of the noise.
        - octaves (int): The number of octaves in the noise.
        - seed (int): The seed for the noise.

        Returns:
        - List[List[float]]: A 2D array representing the generated Perlin noise.
        """
        noise = PerlinNoise(octaves=octaves, seed=seed)
        noise_values = [[noise([i / scale, j / scale]) for j in range(width)] for i in range(height)]
        return noise_values

    @staticmethod
    def plot_2d_perlin_noise(noise_values):
        """
        Plot 2D Perlin noise.

        Parameters:
        - noise_values (List[List[float]]): 2D array representing the generated Perlin noise.

        Returns:
        - None: Displays the plot.
        """
        plt.imshow(noise_values, cmap="viridis", origin="lower")
        plt.colorbar()
        plt.show()

    @staticmethod
    def plot_3d_perlin_noise(width, height, depth, scale, octaves, seed):
        """
        Plot 3D Perlin noise.

        Parameters:
        - width (int): The width of the noise grid.
        - height (int): The height of the noise grid.
        - depth (int): The depth of the noise grid.
        - scale (float): The scale of the noise.
        - octaves (int): The number of octaves in the noise.
        - seed (int): The seed for the noise.

        Returns:
        - None: Displays the 3D plot.
        """
        noise = PerlinNoise(octaves=octaves, seed=seed)
        noise_values = [[[noise([i / scale, j / scale, k / scale]) for k in range(depth)] for j in range(height)] for i in range(width)]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        x, y, z = np.meshgrid(range(width), range(height), range(depth))
        ax.scatter(x, y, z, c=noise_values, cmap="viridis", marker=".")
        plt.show()
