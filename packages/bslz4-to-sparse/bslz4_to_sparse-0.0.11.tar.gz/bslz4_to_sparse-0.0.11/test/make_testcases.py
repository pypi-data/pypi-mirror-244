

import hdf5plugin, h5py, numpy as np, os, sys

def write_array( h5name, dsetname, ary ):
    assert len(ary.shape) == 3
    with h5py.File( h5name, "a" ) as h5f:
        # Hard wire the bitshuffle numbers
        dset = h5f.create_dataset( dsetname, data = ary,
                                   chunks = (1, ary.shape[1], ary.shape[2]),
                                   compression = 32008,
                                   compression_opts = (0,2), )
        print("Wrote",h5name,dsetname)


METHODS = {
    # use less disk space:
    'uniform15' : lambda nelem, dt : np.random.randint( 0, 15, size=nelem, dtype = dt ),
    'Poisson_1'  : lambda nelem, dt : np.random.poisson( lam=1.0, size=nelem ).astype( dt ),
    # Range for debugging. Gives the array indices in output in small blocks
    'Range_31' :  lambda nelem, dt : ( (1/31)*np.arange( 0, nelem, dtype=np.float32 )).astype( dt ),
    # Random numbers. Hard to look at but hopefully a stringent test as they should not compress.
    'uniform_random' : lambda nelem, dt : np.random.randint( 0, pow(2,8*dt(0).itemsize),
                                                            size=nelem, dtype = dt ),
    # Poisson random numbers. For timing:
    'Poisson_0.01' : lambda nelem, dt : np.random.poisson( lam=0.01, size=nelem).astype( dt ),
    'Poisson_100'  : lambda nelem, dt : np.random.poisson( lam=100.0, size=nelem).astype( dt ),
    # Range for debugging. Gives the array indices in output
    '1_Range_1' :  lambda nelem, dt : np.arange( nelem, dtype = dt ),
    # Range for debugging. Gives the array indices in output in blocks
    'Range_1024' : lambda nelem, dt : ( (1./1024)*np.arange( 0, nelem, dtype=np.float32 )).astype( dt ),
}

N = 2
BIG = [ ('Frelon2K', (N, 2048, 2048) ),
        ('Eiger4M' , (N, 2162, 2068) ),
        ('Primes'  , (N, 521, 523) ) ]

SMALL = [ ('256 square', (N, 256, 256) ),
          ('Small Primes', (N, 149, 211) ),]

def make_testcases( hname, cases ) :
    np.random.seed(10007*10009)
    for name, shp in cases:
        for dtyp, label in ( ( np.uint8 , 'u8' ),
                             ( np.uint16, 'u16' ),
                             ( np.uint32, 'u32' ) ):
            ary = np.empty( shp, dtype = dtyp )
            for i, method in enumerate(METHODS):
                ary = METHODS[method]( ary.size, dtyp ).reshape( shp )
                print(method, ary.mean(dtype=float), ary.std())
                dsname = "_".join((name, label, method))
                write_array( hname, dsname , ary )






if __name__=="__main__":
    hname = "bslz4testcases.h5"
    if os.path.exists(hname):
        print("Removed", hname)
        os.remove(hname)
    if len(sys.argv)>1 and sys.argv[1]=='all':
        make_testcases(hname, SMALL+BIG )
    else:
        make_testcases(hname, SMALL )




