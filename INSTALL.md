# Build the environment on your mac.

1. Install numpy in the arm environment
```
  pip install numpy numpy scipy Cython
```
2. Check installed modules
```
  2.1 go into python and use this command: help("modules")
  2.2 pip freeze
```
3. Build and install zlib
```
  ZDIR=/usr/local
  ./configure --prefix=${ZDIR}
  make check
  make install
```
4. Build and install HDF5
```
  H5DIR=/usr/local
  ./configure --with-zlib=${ZDIR} --prefix=${H5DIR} --enable-hl --enable-shared
  make check
  make install
```
5. Build and install netCDF-4 C lib
```
  NCDIR=/usr/local
  CPPFLAGS=-I${H5DIR}/include LDFLAGS=-L${H5DIR}/lib ./configure --prefix=${NCDIR} --enable-netcdf-4 --enable-shared
  make check
  make install
```
6. Install netCDF python package
```
  download the latest source code from github https://github.com/Unidata/netcdf4-python
  python setup.py build
  python setup.py install
```
7. To run all the tests, execute 
```
  cd test && python run_all.py
```
netcdf files from ARM use time as dim, 1440 currently

# Examples of common uses of ncdump
1. To look at just the header information (also called the schema or metadata):
```
ncdump -h sgp.cdf 
```
2. To look at header and coordinate information, but not the data:
```
ncdump -c sgp.cdf
```
3. To look at all the data in the file, in addition to the metadata:
```
ncdump sgp.cdf
```
4. To look at a subset of the data by specifying one or more variables:
```
ncdump -v lat,time sgp.cdf
```
5. To see times in human-readable form:
```
ncdump -t -v lat,time sgp.cdf
```
6. To look at what kind of netCDF data is in the file (classic, 64-bit offset, netCDF-4, or netCDF-4 classic model):
```
ncdump -k sgp.cdf
```
