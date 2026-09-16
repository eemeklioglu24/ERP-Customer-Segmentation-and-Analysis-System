import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial as spa
from sklearn.metrics import silhouette_score

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
    cluster_names = ['Küme 1', 'Küme 2', 'Küme 3', 'Küme 4', 'Küme 5', 'Küme 6', 'Küme 7', 'Küme 8', 'Küme 9', 'Küme 10', 'Küme 11', 'Küme 12']
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('Son Alışverişten Geçen Süre')
    ax.set_ylabel('İşlem Sayısı')
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
        
    

def find_and_plot_clusters(X, N, K):
    centroids = None
    memberships = None
    iteration = 1
    while True:
        if iteration == 210:
            break

        old_centroids = centroids
        centroids = update_centroids(memberships, X, N, K)
        if np.all(centroids == old_centroids):
            break
        old_memberships = memberships
        memberships = update_memberships(centroids, X)
        if np.all(memberships == old_memberships):
            plot_current_state(centroids, memberships, X, K)
            plt.title("Iteration: " + str(iteration))
            print(f"Total Iterations: {iteration}")
            plt.show()
            break
        # else:
        #     plot_current_state(centroids, memberships, X, K)
        #     plt.title(str(iteration))
        #     plt.show()

        iteration = iteration + 1
    return memberships, centroids

def k_means_clustering(X, N, K):
    # Finds a single run of K Means clustering that gives the runs own objective, memberships and centrids
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
    return(current_objective, memberships, centroids)

def get_obj(X, N, n_init= 5):
    objective_values = []
    silhouette_scores = []
    for K in np.arange(2, 11):
        objective, silhoutte, centroids= k_means_clustering(X, N, K)
        objective_values.append(objective)
        score = silhouette_score(X, silhoutte)
        silhouette_scores.append(score)  
    # plt.figure(figsize = (8, 4))
    # plt.plot(np.arange(2, 11), objective_values, "o-")
    # plt.xlabel("$K$")
    # plt.ylabel("Objective value")
    # plt.show()

    # plt.plot(np.arange(2, 11), silhouette_scores, marker="o")
    # plt.xlabel("Number of Clusters (K)")
    # plt.ylabel("Silhouette Score")
    # plt.title("Silhouette Score by K")
    # plt.show()
    return objective_values, silhouette_scores

def best_k_means_run(X, N, K, n_init):
    best_objective = float("inf")
    best_membership = None
    best_centroid = None
    for _ in range(n_init):
        objective, memberships, centroids = k_means_clustering(X, N, K)
        
        if objective < best_objective:
            best_objective = objective
            best_membership = memberships
            best_centroid = centroids
    return  (best_objective, best_membership, best_centroid)

def robust_kmeans(X, N, K, n_init= 5):
    objective_values = []
    silhouette_scores = []

    best_membership = None
    best_centroid = None

    for k in range(2, 11):

        objective, memberships, centroids = best_k_means_run(
            X, N, k, n_init
        )

        objective_values.append(objective)

        score = silhouette_score(X, memberships)
        silhouette_scores.append(score)

        if k == K:
            best_membership = memberships.copy()
            best_centroid = centroids.copy()

    return (
        objective_values,
        best_membership,
        best_centroid,
        silhouette_scores
    )

def test_robustness(X, N, K, n_runs=20):
    objectives = []
    silhouettes = []

    for _ in range(n_runs):
        objective, memberships, centroids = (
            k_means_clustering(X, N, K)
        )
        objectives.append(objective)
        score = silhouette_score(X,memberships)
        silhouettes.append(score)

    return objectives, silhouettes
    
