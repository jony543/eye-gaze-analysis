import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
from sys import platform


class TrialColorPlot:
    def xy(self, df, stim_img, screen_resolution):
        def plot_xy(ax):
            z = df['timestamp'].to_numpy()
            norm = np.linalg.norm(z)
            min_z = np.min(z)

            ax.scatter(df['rx'].to_numpy(), df['ry'].to_numpy(), c=(z - min_z) / norm, cmap=plt.get_cmap('viridis'))

            plt.xlim([0, screen_resolution[0]])
            plt.ylim([0, screen_resolution[1]])

        return self.plot_single_graph_with_image(stim_img, screen_resolution, plot_xy)

    def polar(self, df, stim_img, screen_resolution):
        def plot_polar(ax):
            z = df['timestamp'].to_numpy()
            norm = np.linalg.norm(z)
            min_z = np.min(z)

            ax.scatter(df['alpha'].to_numpy(), df['radius'].to_numpy(), c=(z - min_z) / norm, cmap=plt.get_cmap('viridis'))

        return self.plot_single_graph(plot_polar)

    def plot_single_graph_with_image(self, image, screen_resolution, func):
        def plot_single_graph_with_image_internal(ax):
            im = img.imread(image)

            im_h = im.shape[0]
            im_w = im.shape[1]
            x_margin = (screen_resolution[0] - im_w) / 2
            y_margin = (screen_resolution[1] - im_h) / 2

            plt.imshow(im, origin='upper', extent=(x_margin, x_margin + im_w, y_margin, y_margin + im_h))

            func(ax)

        return self.plot_single_graph(plot_single_graph_with_image_internal)

    def plot_single_graph(self, func):
        fig = plt.figure(1)
        ax = plt.subplot(111) #, projection='polar')

        func(ax)

        if 'linux' in platform:
            plt.savefig('output.png')
        else:
            plt.show()

        return fig
