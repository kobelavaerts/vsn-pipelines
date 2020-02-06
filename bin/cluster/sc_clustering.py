#!/usr/bin/env python3

import argparse
import os
import scanpy as sc

parser = argparse.ArgumentParser(
    description='',
    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument(
    "input",
    type=argparse.FileType('r'),
    help='Input h5ad file.'
)

parser.add_argument(
    "output",
    type=argparse.FileType('w'),
    help='Output h5ad file.'
)

parser.add_argument(
    "-x", "--method",
    type=str,
    action="store",
    dest="method",
    default="louvain",
    choices=['louvain', 'leiden'],
    help="""
         Cluster cells using one of the following algorithms:
         - the Louvain algorithm [Blondel et al. (2008)] in the implementation of [Traag (2017)].
         - the Leiden algorithm [Traag18], an improved version of the Louvain algorithm [Blondel08]. It has been proposed for single-cell analysis by [Levine15].
         """
)

parser.add_argument(
    "-r", "--resolution",
    type=float,
    action="store",
    dest="resolution",
    default=1.0,
    help="""
         louvain: For the default flavor ('vtraag'), you can provide a resolution (higher resolution means finding more and smaller clusters
         leiden: A parameter value controlling the coarseness of the clustering. Higher values lead to more clusters. Set to None if overriding partition_type to one that doesn’t accept a resolution_parameter.
         """
)

args = parser.parse_args()

# Define the arguments properly
FILE_PATH_IN = args.input
FILE_PATH_OUT_BASENAME = os.path.splitext(args.output.name)[0]

# I/O
# Expects h5ad file
try:
    adata = sc.read_h5ad(filename=FILE_PATH_IN.name)
except IOError:
    raise Exception("Can only handle .h5ad files.")


def check_neighborhood_graph_exists(adata):
    if "neighbors" not in adata.uns.keys():
        raise Exception(
            "The neighborhood graph of observations has not been computed. Please do so before running {} clustering".format(
                args.method)
        )

#
# Clustering the data
#


if args.method.lower() == "louvain":
    # Run Louvain clustering
    # Source: https://icb-scanpy.readthedocs-hosted.com/en/stable/api/scanpy.tl.louvain.html
    check_neighborhood_graph_exists(adata=adata)
    sc.tl.louvain(
        adata,
        resolution=args.resolution
    )
elif args.method.lower() == "leiden":
    # Run Leiden clustering
    # Source: https://icb-scanpy.readthedocs-hosted.com/en/stable/api/scanpy.tl.leiden.html
    check_neighborhood_graph_exists(adata=adata)
    sc.tl.leiden(
        adata,
        resolution=args.resolution
    )
else:
    raise Exception("The given clustering algorithm {} does not exist or is not implemeted.".format(args.method))

# I/O
adata.write_h5ad("{}.h5ad".format(FILE_PATH_OUT_BASENAME))
