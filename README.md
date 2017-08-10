Dependencies:

- Requires Python 2.*.


Calculates the Omega Index as described in Collins and Dent 1988
Takes two solution files as parameters and compares them.
Each file should be delimited by tabs or spaces, where the first column contains the object IDs and subsequent columns list the cluster/community IDs for each object, e.g.:

```
A       1
B       1
C       1
D       1       2
E       2
F       2
G       2
H       3
I       3
J       4
```
Note that objects can belong to more than one cluster/community, i.e. overlap is allowed.
Note also that this is very slow with large networks, e.g. > 2000 objects/nodes, because it involves looking at every pairing of objects (AB, AC, AD...IJ).

--

If you use this code in your own research, please consider citing the following paper:

```
@inproceedings{murray2012using,
  title={Using the omega index for evaluating abstractive community detection},
  author={Murray, Gabriel and Carenini, Giuseppe and Ng, Raymond},
  booktitle={Proceedings of Workshop on Evaluation Metrics and System Comparison for Automatic Summarization},
  pages={10--18},
  year={2012},
  organization={Association for Computational Linguistics}
}
```
