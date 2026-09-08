import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial as spa

def update_centroids(memberships, X, N, K):
    if memberships is None:
        # initialize centroids
        centroids = X[np.random.choice(range(N), K, False), :]
    else:
        # update centroids
        centroids = np.vstack([np.mean(X[memberships == k, :], axis = 0) for k in range(K)])
    return(centroids)

def update_memberships(centroids, X):
    # calculate distances between centroids and data points
    D = spa.distance_matrix(centroids, X)
    # find the nearest centroid for each data point
    memberships = np.argmin(D, axis = 0)
    return(memberships)

def plot_current_state(centroids, memberships, X, K):
    cluster_colors = np.array(["#1f78b4", "#33a02c", "#e31a1c", "#ff7f00", "#6a3d9a", "#b15928",
                               "#a6cee3", "#b2df8a", "#fb9a99", "#fdbf6f", "#cab2d6", "#ffff99"])
    if memberships is None:
        plt.plot(X[:, 0], X[:, 1], ".", markersize = 10, color = "black")
    else:
        for c in range(K):
            plt.plot(X[memberships == c, 0], X[memberships == c, 1], ".", markersize = 10,
                     color = cluster_colors[c])
    for c in range(K):
        plt.plot(centroids[c, 0], centroids[c, 1], "s", markersize = 12, 
                 markerfacecolor = cluster_colors[c], markeredgecolor = "black")
    plt.xlabel("$x_1$")
    plt.ylabel("$x_2$")

def plot_clusters(X, N, K):
    centroids = None
    memberships = None
    iteration = 1
    while True:
        if iteration == 21:
            break
        print("Iteration#{}:".format(iteration))

        old_centroids = centroids
        centroids = update_centroids(memberships, X, N, K)
        if np.all(centroids == old_centroids):
            break
        else:
            plt.figure(figsize = (12, 6))    
            plt.subplot(1, 2, 1)
            plot_current_state(centroids, memberships, X, K)

        old_memberships = memberships
        memberships = update_memberships(centroids, X)
        if np.all(memberships == old_memberships):
            plt.subplot(1, 2, 2)
            plt.axis("off")
            plt.show()
            break
        else:
            plt.subplot(1, 2, 2)
            plot_current_state(centroids, memberships, X)
            plt.show()

        iteration = iteration + 1

def k_means_clustering(X, N, K):
    objective_value = 1e20
    for replication in range(100):
        centroids = None
        memberships = None
        iteration = 1
        while True:
            if iteration == 101:
                break

            old_centroids = centroids
            centroids = update_centroids(memberships, X, N, K)
            if np.all(centroids == old_centroids):
                break

            old_memberships = memberships
            memberships = update_memberships(centroids, X)
            if np.all(memberships == old_memberships):
                break

            iteration = iteration + 1
        D = spa.distance_matrix(centroids, X)
        current_objective = np.sum(np.min(D, axis = 0)**2)
        if current_objective < objective_value:
            objective_value = current_objective
    return(objective_value)