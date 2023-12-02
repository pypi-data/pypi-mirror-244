try:
    import mpi4py.MPI
except ImportError:
    _comm = None
    has_mpi = False
    main_node = True
else:
    _comm = mpi4py.MPI.COMM_WORLD
    has_mpi = True
    main_node = not _comm.Get_rank()


def set_comm(comm):
    global _comm

    _comm = comm


def barrier():
    if _comm:
        _comm.barrier()


def bcast(data, root=0):
    if not _comm:
        return data
    else:
        return _comm.bcast(data, root=root)
