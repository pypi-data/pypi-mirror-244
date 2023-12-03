""" This module contains all helper functions not core to the models.
"""
import numpy as np
from numba import njit
from numpy.random import default_rng
import scipy.sparse as sp
import os
import numpy.random as rng
from math import isinf
import graph_ensembles.methods as mt
from NEMtropy import models_functions as mof
from NEMtropy import solver_functions as sof
from sklearn.metrics.pairwise import pairwise_distances


# Simulation helper functions
def firm_filter(W, C, G):
    """Iteratively eliminate firms that have zero input or zero production."""
    new_W = W.copy()
    new_C = C.copy()
    G_mat = G.copy()

    while True:
        N = len(new_C)
        nnz_rows, nnz_cols = new_W.nonzero()
        nnz_output = set(nnz_cols) | set(new_C.nonzero()[0])
        nnz_input = set(nnz_rows)
        to_keep_ind = list(np.sort(list(nnz_output & nnz_input)))

        if len(to_keep_ind) == N:
            return new_W, new_C, G_mat
        else:
            new_W = new_W[to_keep_ind][:, to_keep_ind]
            new_C = new_C[to_keep_ind]
            G_mat = G_mat[:, to_keep_ind]


# Network margins generating functions
def get_sector_definitions(N, S_io, r_n_s):
    """Assign firms to each group of the IO table."""
    # Get number of firms per sector ensuring sum is N
    msg = "Relative number of firms per sector does not match number of " "sectors."
    assert len(r_n_s) == S_io, msg
    msg = "Relative number of firms must sum to one."
    assert abs(r_n_s.sum() - 1) < 1e-9, msg
    n_s = np.floor(r_n_s * N).astype(np.int64)
    n_s[np.argsort(r_n_s * N)[: np.int64(N - n_s.sum())]] += 1

    # Construct dictionary of industry groups
    industry_dict = {}
    n_s_csum = np.cumsum(n_s)
    G_io = np.zeros((S_io, N), dtype=np.uint8)
    j = 0
    for i in range(N):
        if i >= n_s_csum[j]:
            j += 1
        industry_dict[i] = j
        G_io[j, i] = 1

    return n_s, G_io, industry_dict


def sample_strength_out(N, Z, n_s, cv, G_io):
    """Returns a sample of out strength by sector taken from a log-normal
    distribution with given coefficient of variation.
    """
    # Sample firm out strength
    rng = default_rng()
    s_out = np.zeros((N, G_io.shape[0]), dtype=np.float64)

    for i, sout in enumerate(Z.sum(axis=1)):
        # Sample n elements such that they have the correct mean value
        # as well as the correct coefficient of variation cv
        s_sqr = np.log(cv**2 + 1)
        m = np.log(Z.sum() / n_s[i]) - s_sqr / 2
        s = np.sqrt(s_sqr)
        vals = rng.lognormal(mean=m, sigma=s, size=n_s[i])
        assert vals.dtype == np.float64, "Random numbers must be 64-bits"

        # Scale to ensure exact match of total flows
        mult = sout / vals.sum()
        idx_i = np.where(G_io[i])[0]
        s_out[idx_i, i] = vals * mult

    # Test that the out strength sums to the IO elements
    assert np.allclose(np.dot(G_io, s_out).sum(axis=1), Z.sum(axis=1))

    return s_out


def sample_final_demand(N, C, s_out, G_io, eps):
    """Assigns to each firm a final demand value based on the industry total."""
    rng = default_rng()
    c = s_out.sum(axis=1) * rng.normal(loc=1.0, scale=eps, size=N)
    assert c.dtype == np.float64, "Random numbers must be 64-bits"
    c *= (G_io * (C / np.dot(G_io, c)).reshape((G_io.shape[0], 1))).sum(axis=0)

    # Ensure total demands sums to IO values
    assert np.allclose(np.dot(G_io, c), C)
    return c


def sample_homogeneous_s_in(N, Z, s_out, c, G_io):
    """Generate the in strengths of all firms based on the aggregate
    production function of their industry.
    """
    p = s_out.sum(axis=1) + c
    P = np.dot(G_io, p)
    agg_p_coef = Z / P
    assert np.allclose(Z, agg_p_coef * P)
    assert np.allclose(
        np.dot(np.linalg.inv(np.eye(G_io.shape[0]) - agg_p_coef), np.dot(G_io, c)), P
    )

    # Get strength in by sector from production level
    s_in = np.dot(agg_p_coef, G_io).T
    s_in *= p.reshape(N, 1)
    assert np.allclose(np.dot(G_io, s_in).T, Z)

    return s_in


def get_number_links(d, N, n_s, s_in, G_io):
    # Total number of links in the network
    L = np.int64(np.round(d * N * (N - 1)))

    # For each sector find the maximum number of connections
    l_s_max = n_s * np.sum(s_in != 0, axis=0)

    # Remove self-loop contributions
    l_s_max -= np.sum((s_in * G_io.T) != 0, axis=0)

    # Define new density as the density of realizable connections
    d_tilde = L / np.sum(l_s_max)

    # Get number of links per sector ensuring sum is L
    l_s = np.floor(l_s_max * d_tilde).astype(np.int64)
    l_s[np.argsort(l_s_max * d_tilde)[: np.int64(L - l_s.sum())]] += 1

    return l_s


# Network generating functions
@njit
def random_first_edge(s_out, s_in, N, G_io):
    # Assign to each node one random link from the available set
    unlinked_out = list(range(N))
    edge_list = []

    # First loop ensures every node has one incoming link
    for i, s_in_i in enumerate(s_in):
        # Get set of possible node to connect to
        possible_j = []
        for x in np.where(s_in_i != 0)[0]:
            possible_j.extend(np.where(G_io[x, :])[0])

        possible_j = np.array(possible_j)

        # Check that there are unlinked ones in the possible set
        possible_j_unlinked = np.array(
            list(set(possible_j).intersection(set(unlinked_out)))
        )

        # Select one random link
        if len(possible_j_unlinked) > 0:
            sample = rng.choice(possible_j_unlinked)
            unlinked_out.remove(sample)
        else:
            sample = rng.choice(possible_j)

        # Add edge to list
        edge_list.append([sample, i])

    # Second loop guarantees at least one outgoing link
    for i in unlinked_out:
        # Get industry of outgoing link
        industry = np.where(G_io[:, i])[0][0]

        # Get all possible links with in strength different from zero
        possible_j = np.where(s_in[:, industry] != 0)[0]

        # Select one random link
        sample = rng.choice(possible_j)

        # Add edge to list
        edge_list.append([i, sample])

    return edge_list


@njit
def edges_per_layer(edge_list, S_io, industry_arr):
    l_s_sampled = np.zeros(S_io, dtype=np.int64)
    for e in edge_list:
        # Add to sector layer of out node one link
        l_s_sampled[industry_arr[e[0]]] += 1

    return l_s_sampled


def residual_l_by_sector(l_s, l_s_sampled):
    # Get desired vs sampled number of links per layer
    l_s_temp = l_s - l_s_sampled

    # Compute negative links to be removed from other layers
    extra_l = -l_s_temp[l_s_temp < 0].sum()

    # Set all layers to be positive
    l_s_temp[l_s_temp < 0] = 0

    # Get total links missing
    L_tilde = l_s_temp.sum() - extra_l

    # Ensure that there is a positive number of missing links
    if L_tilde <= 0:
        return np.zeros(l_s.shape, dtype=np.int64)

    # Reduce proportionally remaining links ensuring exact match
    l_s_tilde = np.floor(l_s_temp * (L_tilde / l_s_temp.sum())).astype(np.int64)
    l_s_tilde[
        np.argsort(l_s_temp * (L_tilde / l_s_temp.sum()))[
            : np.int64(L_tilde - l_s_tilde.sum())
        ]
    ] += 1

    return l_s_tilde


@njit
def layer_f_jac_exclusion(z, ind_out, fit_out, ind_in, fit_in, n_edges, exclusions):
    """Compute the objective function of the newton solver and its
    derivative for a single label of the stripe model excluding
    certain i,j combinations.
    """
    jac = 0
    f = 0
    for n, i in enumerate(ind_out):
        excluded_j = exclusions[exclusions[:, 0] == i][:, 1]
        for m, j in enumerate(ind_in):
            if (i != j) and (j not in excluded_j):
                tmp = fit_out[n] * fit_in[m]
                tmp1 = z * tmp
                if isinf(tmp1):
                    f += 1
                    jac += 0
                else:
                    f += tmp1 / (1 + tmp1)
                    jac += tmp / (1 + tmp1) ** 2

    return f - n_edges, jac


def fit_residual(l_s_tilde, s_out, s_in, edge_list, S_io):
    solver_output = [None] * S_io
    z_fit = np.zeros(S_io, dtype=np.float64)

    for i in range(S_io):
        n_edges = l_s_tilde[i]
        if n_edges == 0:
            continue

        ind_out = s_out.indices[s_out.indptr[i] : s_out.indptr[i + 1]]
        fit_out = s_out.data[s_out.indptr[i] : s_out.indptr[i + 1]]
        ind_in = s_in.indices[s_in.indptr[i] : s_in.indptr[i + 1]]
        fit_in = s_in.data[s_in.indptr[i] : s_in.indptr[i + 1]]

        solver_output[i] = mt.newton_solver(
            x0=0,
            fun=lambda x: layer_f_jac_exclusion(
                x, ind_out, fit_out, ind_in, fit_in, n_edges, edge_list
            ),
            tol=1e-5,
            xtol=1e-12,
            max_iter=100,
            verbose=False,
            full_return=True,
        )

        if not solver_output[i].converged:
            print("Layer {} did not converge".format(i))
        z_fit[i] = solver_output[i].x

    return z_fit


@njit
def layer_sample(z, ind_out, fit_out, ind_in, fit_in, exclusions):
    """Sample residual edges."""
    sample = []
    for n, i in enumerate(ind_out):
        excluded_j = exclusions[exclusions[:, 0] == i][:, 1]
        for m, j in enumerate(ind_in):
            if (i != j) and (j not in excluded_j):
                tmp = z * fit_out[n] * fit_in[m]
                if isinf(tmp):
                    pij = 1
                else:
                    pij = tmp / (1 + tmp)

                if rng.random() < pij:
                    sample.append([i, j])

    return sample


def sample_residual_links(z_fit, s_out, s_in, edge_list, S_io):
    new_edges = []
    for i in range(S_io):
        z = z_fit[i]
        if z == 0:
            continue

        ind_out = s_out.indices[s_out.indptr[i] : s_out.indptr[i + 1]]
        fit_out = s_out.data[s_out.indptr[i] : s_out.indptr[i + 1]]
        ind_in = s_in.indices[s_in.indptr[i] : s_in.indptr[i + 1]]
        fit_in = s_in.data[s_in.indptr[i] : s_in.indptr[i + 1]]

        new_edges.extend(layer_sample(z, ind_out, fit_out, ind_in, fit_in, edge_list))

    return new_edges


def filter_scale_sin(edge_list, s_in, s_out, industry_arr):
    # Transform edge list i to sector
    sect_list = np.unique([[industry_arr[i], j] for i, j in edge_list], axis=0)

    # Initialise filtered s_in
    s_in_filtered = np.zeros(s_in.shape, dtype=np.float64)

    # Correct s_in to put zero where there is no link to that sector
    for sect, j in sect_list:
        # Set to the original value the strengths that have a link
        s_in_filtered[j, sect] = s_in[j, sect]

    # Compute the s_in to reassign
    missing_sin = (s_in - s_in_filtered).sum(axis=0).A1

    # Scale to match
    scaler = 1 + missing_sin / s_in_filtered.sum(axis=0)
    s_in_filtered *= scaler

    # Check that it matches
    assert np.allclose(s_in_filtered.sum(axis=0), s_in.sum(axis=0))
    assert np.allclose(s_in_filtered.sum(axis=0), s_out.sum(axis=0))

    return s_in_filtered


@njit
def weight_sample(edge_list, out_ind, s_out, in_ptr, in_ind, s_in, W):
    # Initialize weigths of sampled edges
    weights = np.empty(len(edge_list), dtype=np.float64)

    for n, (i, j) in enumerate(edge_list):
        # Identify product layer from out strength
        sect = out_ind[i]

        # Get out strength
        x_i = s_out[i]

        # Get in strength of correct product
        j_sects = in_ind[in_ptr[i] : in_ptr[i + 1]]
        j_vals = s_in[in_ptr[i] : in_ptr[i + 1]]
        x_j = j_vals[j_sects == sect][0]

        # Sample weight from exponential
        weights[n] = rng.exponential(x_i * x_j / W[sect])

    return weights


def crema_fit_layer(sect, adj, s_out_l, s_in_l, indptr, N):
    # Parametrize solver
    args = (s_out_l, s_in_l, adj, np.nonzero(s_out_l)[0], np.nonzero(s_in_l)[0])

    # Set initial conditions
    b_out = (s_out_l > 0).astype(np.float64) / (s_out_l + 1)
    b_in = (s_in_l > 0).astype(np.float64) / (s_in_l + 1)
    x0 = np.concatenate((b_out, b_in))

    # Select functionals
    def fun(x):
        return -mof.loglikelihood_prime_crema_directed(x, args)

    def fun_jac(x):
        return -mof.loglikelihood_hessian_diag_crema_directed(x, args)

    def step_fun(x):
        return -mof.loglikelihood_crema_directed(x, args)

    def fun_linsearch(x):
        return mof.linsearch_fun_crema_directed(
            x, (mof.loglikelihood_crema_directed, args)
        )

    reg_fun = sof.matrix_regulariser_function

    # Solve
    sol = sof.solver(
        x0,
        fun=fun,
        fun_jac=fun_jac,
        step_fun=step_fun,
        linsearch_fun=fun_linsearch,
        hessian_regulariser=reg_fun,
        tol=1e-3,
        eps=1e-3,
        max_steps=500,
        method="quasinewton",
        verbose=False,
        regularise=True,
        regularise_eps=1e-3,
        linsearch=True,
        full_return=True,
    )

    return sol


@njit
def crema_sample_layer(b_out_s, b_in_s, adj, N):
    # Initialize weigths of sampled edges
    weights = np.empty(len(adj[0]), dtype=np.float64)

    rows = adj[0]
    cols = adj[1]
    vals = adj[2]

    for n, (i, j, v) in enumerate(zip(rows, cols, vals)):
        exp_w_ij = v / (b_out_s[i] + b_in_s[j])
        weights[n] = rng.exponential(exp_w_ij)

    return weights


def crema_weight_sample(edge_list, s_out, s_in, n_s, N):
    # Initialize weigths of sampled edges
    weights = np.empty(len(edge_list), dtype=np.float64)

    for sect in range(len(n_s)):
        # Get sector indices
        indptr = np.append([0], np.cumsum(n_s))

        # Select specific layer strengths
        s_out_l = np.zeros(N, dtype=np.float64)
        s_out_l[s_out[:, sect] != 0] = s_out[s_out[:, sect] != 0, sect]
        s_in_l = np.zeros(N, dtype=np.float64)
        s_in_l[s_in[:, sect] != 0] = s_in[s_in[:, sect] != 0, sect]

        # Select edges belonging to the layer
        e_sect_ind = [
            (indptr[sect] <= x) and (x < indptr[sect + 1]) for x in edge_list[:, 0]
        ]
        adj = (
            edge_list[:, 0][e_sect_ind],
            edge_list[:, 0][e_sect_ind],
            np.ones(np.sum(e_sect_ind)),
        )

        # Fit crema for layer
        sol = crema_fit_layer(sect, adj, s_out_l, s_in_l, indptr, N)

        # Get parameters from solution
        b_out_s = sol[0][:N]
        b_in_s = sol[0][N : 2 * N]

        # Sample weights
        weights[e_sect_ind] = crema_sample_layer(b_out_s, b_in_s, adj, N)

    return weights


# Saving and loading adjacency matrices
def case_name(N, d, cv, eps):
    """Returns the case name for the given parameters."""
    tmp = ["N", N, "d", d, "cv", cv, "e", eps]
    tmp_s = [str(x) for x in tmp]
    return "{}/".format("_".join(tmp_s))


def save_W(filename, W):
    if isinstance(W, sp.spmatrix):
        sp.save_npz(filename + ".npz", W)
    elif isinstance(W, list):
        os.mkdir(filename)
        for i, w in enumerate(W):
            sp.save_npz(filename + "/" + str(i) + ".npz", w)


def load_W(filename, compress=True):
    try:
        return sp.load_npz(filename + ".npz")
    except FileNotFoundError:
        dirs = os.listdir(filename)
        n = len(dirs)
        if compress:
            W = sp.load_npz(filename + "/0.npz")
            for i in range(1, n):
                W += sp.load_npz(filename + "/" + str(i) + ".npz")
        else:
            W = []
            for i in range(n):
                W.append(sp.load_npz(filename + "/" + str(i) + ".npz"))
        return W


# Plotting functions
def pmf(a):
    x, counts = np.unique(a, return_counts=True)
    return x, counts / len(a)


def cdf(a, start=0):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts) + start
    y = cusum / cusum[-1]
    x = np.insert(x, 0, x[0])
    y = np.insert(y, 0, start / cusum[-1])
    return x, y


def icdf(a):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts)
    y = 1 - cusum / cusum[-1]
    y = np.insert(y, 0, 1)
    return x, y[:-1]


# NUMBA acceleration functions
@njit
def faster_dot(ind, ptr, dat, v, dtype):
    res = np.zeros(len(ptr) - 1, dtype=dtype)
    for j in range(len(v)):
        if v[j] != 0:
            rows = ind[ptr[j] : ptr[j + 1]]
            for n in range(len(rows)):
                res[rows[n]] += v[j] * dat[ptr[j] + n]

    return res


# Other functions
def name_sim(a, b):
    # Extract words eliminating conjunctions
    conj = {"and", "of"}
    a = set(a.lower().replace(",", "").split()) - conj
    b = set(b.lower().replace(",", "").split()) - conj

    # Compute overlap
    return len(a.intersection(b)) / len(a)


# Production function distance measures
def return_summed_array(take_array, num_sect, a_dict):
    new_vect = []

    for j in range(num_sect):
        keys = [k for k, v in a_dict.items() if v == j]
        new_vect.append(np.sum([take_array[keys]]))

    return new_vect


def new_eff_jacc(tech_c, dict_t, num_sect):
    """Similarity averaging (or summing) over sectors' inputs."""

    rows_m = []
    rows_sd = []
    cols_m = []
    cols_sd = []
    sector_rows_m = []
    sector_cols_m = []
    sector_rows_sd = []
    sector_cols_sd = []

    for i in range(num_sect):
        keys = [k for k, v in dict_t.items() if v == i]

        # Try to get IO rows/columns to benchmark het. measure
        cols_io = tech_c[:, list(keys)]
        sum_cols = cols_io.sum(axis=1)
        sum_over_cols = return_summed_array(sum_cols, num_sect, dict_t)
        bin_io_cols = np.where(np.array(sum_over_cols) > 0, 1, 0)

        rows_io = tech_c[list(keys), :]
        sum_rows = rows_io.sum(axis=0)
        sum_over_rows = return_summed_array(sum_rows.T, num_sect, dict_t)
        bin_io_rows = np.where(np.array(sum_over_rows) > 0, 1, 0)

        X = []
        X.append(np.array(bin_io_cols))
        Y = []
        Y.append(np.array(bin_io_rows).T)

        for j in keys:
            cols_single = tech_c[:, list(dict_t).index(j)]
            rows_single = tech_c[list(dict_t).index(j), :]

            single_col = return_summed_array(cols_single, num_sect, dict_t)
            single_row = return_summed_array(rows_single.T, num_sect, dict_t)

            new_binary_cols = np.where(np.array(single_col) > 0, 1, 0)
            new_binary_rows = np.where(np.array(single_row) > 0, 1, 0)

            X.append(np.array(new_binary_cols))
            Y.append(np.array(new_binary_rows))

        X = np.array(X, dtype=bool)
        Y = np.array(Y, dtype=bool)

        jac_col = pairwise_distances(X, metric="jaccard", n_jobs=-1)
        jac_row = pairwise_distances(Y, metric="jaccard", n_jobs=-1)

        mean_col_sector = np.mean(jac_col[0][1:])
        mean_row_sector = np.mean(jac_row[0][1:])

        sd_col_sector = np.std(jac_col[0][1:])
        sd_row_sector = np.std(jac_row[0][1:])

        # Extract all other
        rem_r_c = np.delete(jac_col, (0), axis=0)
        rem_r_c = np.delete(rem_r_c, (0), axis=1)

        rem_r_r = np.delete(jac_row, (0), axis=0)
        rem_r_r = np.delete(rem_r_r, (0), axis=1)

        pair_cols_mean = np.mean(rem_r_c[np.triu_indices(np.shape(rem_r_c)[0], k=1)])
        pair_cols_sd = np.std(rem_r_c[np.triu_indices(np.shape(rem_r_c)[0], k=1)])

        pair_rows_mean = np.mean(rem_r_r[np.triu_indices(np.shape(rem_r_c)[0], k=1)])
        pair_rows_sd = np.std(rem_r_r[np.triu_indices(np.shape(rem_r_c)[0], k=1)])

        # Append to initial arrays
        rows_m.append(pair_rows_mean)
        rows_sd.append(pair_rows_sd)

        cols_m.append(pair_cols_mean)
        cols_sd.append(pair_cols_sd)

        # Append for sectors' comparisons
        sector_rows_m.append(mean_row_sector)
        sector_rows_sd.append(sd_row_sector)

        sector_cols_m.append(mean_col_sector)
        sector_cols_sd.append(sd_col_sector)

    return (
        rows_m,
        rows_sd,
        cols_m,
        cols_sd,
        sector_rows_m,
        sector_rows_sd,
        sector_cols_m,
        sector_rows_sd,
    )
