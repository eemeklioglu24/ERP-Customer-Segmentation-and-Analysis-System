import numpy as np
import matplotlib.pyplot as plt

def generate_random():
    # np.random.seed(421)
    # returns N x 3 random generated data for test purposes.
    N = 500

    # generate random samples
    np.random.multivariate_normal
    X1 = np.random.multivariate_normal(np.array([+2.0, +2.0, +2.0, 0.0]),
                                    np.array([  [0.4, 0.0, 0.0, 0.0],
                                                [0.0, 0.4, 0.0, 0.0],
                                                [0.0, 0.0, 0.4, 0.0],
                                                [0.0, 0.0, 0.0, 0.4]]), N // 4)
    X2 = np.random.multivariate_normal(np.array([+2.0, +2.0, 0.0, 0.0]),
                                    np.array([  [0.4, 0.0, 0.0, 0.0],
                                                [0.0, 0.4, 0.0, 0.0],
                                                [0.0, 0.0, 0.4, 0.0],
                                                [0.0, 0.0, 0.0, 0.4]]), N // 4)
    X3 = np.random.multivariate_normal(np.array([+2.0, 0.0, +2.0, 0.0]),
                                    np.array([  [0.4, 0.0, 0.0, 0.0],
                                                [0.0, 0.4, 0.0, 0.0],
                                                [0.0, 0.0, 0.4, 0.0],
                                                [0.0, 0.0, 0.0, 0.4]]), N // 4)
    X4 = np.random.multivariate_normal(np.array([0.0, +2.0, +2.0, 0.0]),
                                    np.array([  [0.4, 0.0, 0.0, 0.0],
                                                [0.0, 0.4, 0.0, 0.0],
                                                [0.0, 0.0, 0.4, 0.0],
                                                [0.0, 0.0, 0.0, 0.4]]), N // 4)
    # X5 = np.random.multivariate_normal(np.array([2.0, 0.0, 0.0]),
    #                                     np.array([[0.4, 0.0, 0.0],
    #                                                 [0.0, 0.4, 0.0],
    #                                                   [0.0, 0.0, 0.4]]), N // 4)
    # X6 = np.random.multivariate_normal(np.array([0.0, 2.0, 0.0]),
    #                                     np.array([[0.4, 0.0, 0.0],
    #                                                 [0.0, 0.4, 0.0],
    #                                                   [0.0, 0.0, 0.4]]), N // 4)
    # X7 = np.random.multivariate_normal(np.array([0.0, 0.0, 2.0]),
    #                                     np.array([[0.4, 0.0, 0.0],
    #                                                 [0.0, 0.4, 0.0],
    #                                                   [0.0, 0.0, 0.4]]), N // 4)
    # X8 = np.random.multivariate_normal(np.array([0.0, 0.0, 0.0]),
    #                                     np.array([[0.4, 0.0, 0.0],
    #                                                 [0.0, 0.4, 0.0],
    #                                                   [0.0, 0.0, 0.4]]), N // 4)
    X = np.vstack((X1, X2, X3, X4))
    return X, N

def plot_X(X):
    # Plots X to visualize
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(projection='3d')
    ax.plot(X[:, 0], X[:, 1], X[:, 2], ".", markersize=10)
    ax.set_xlabel('Güncellik')
    ax.set_ylabel('Frekans')
    ax.set_zlabel('Parasal Değer')
    ax.set_title("Müşteriler")
    plt.show()