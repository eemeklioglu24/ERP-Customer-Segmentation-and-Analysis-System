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
    cluster_names = ['Küme 1', 'Küme 2', 'Küme 3', 'Küme 4']
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('Güncellik')
    ax.set_ylabel('Frekans')
    ax.set_zlabel('Parasal Değer')
    if memberships is None:
        ax.plot(X[:, 0], X[:, 1], X[:, 2], ".", markersize = 10, color = "black")
    else:
        for c in range(K):
            # ax.plot(X[memberships == c, 0], X[memberships == c, 1], X[memberships == c, 2], ".", markersize = 10,
            #          color = cluster_colors[c])
            ax.scatter(X[memberships == c, 0], X[memberships == c, 1], X[memberships == c, 2], ".",
                     color = cluster_colors[c], label= cluster_names[c])
    for c in range(K):
        ax.plot(centroids[c, 0], centroids[c, 1], centroids[c, 2], "s", markersize = 12, 
                 markerfacecolor = cluster_colors[c], markeredgecolor = "black")
        ax.legend(loc='upper left', frameon=True)
        ax.view_init(vertical_axis= "z")
        
    

def plot_clusters(X, N, K):
    centroids = None
    memberships = None
    iteration = 1
    while True:
        if iteration == 210:
            break
        print("Iteration#{}:".format(iteration))

        old_centroids = centroids
        centroids = update_centroids(memberships, X, N, K)
        if np.all(centroids == old_centroids):
            break
        old_memberships = memberships
        memberships = update_memberships(centroids, X)
        if np.all(memberships == old_memberships):
            plot_current_state(centroids, memberships, X, K)
            plt.title("Iteration: " + str(iteration))
            plt.show()
            break
        # else:
        #     plot_current_state(centroids, memberships, X, K)
        #     plt.title(str(iteration))
        #     plt.show()

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

def get_obj(X, N):
    objective_values = []
    for K in np.arange(1, 11):
        objective_values.append(k_means_clustering(X, N, K))
    plt.figure(figsize = (8, 4))
    plt.plot(np.arange(1, 11), objective_values, "o-")
    plt.xlabel("$K$")
    plt.ylabel("Objective value")
    plt.show()