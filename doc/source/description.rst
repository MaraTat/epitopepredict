Introduction
============

epitopepredict provides a standardized programmatic and command line interface for executing multiple MHC binding prediction methods.
The results from each method can then be processed and visualized in a consistent manner.

Installation
============

This software should be run on a Linux operating system. Ubuntu is recommended but most major distributions will be fine. Windows is not supported. macOS (OS X) may work but has not been tested. If you use windows or a mac you can simply install a linux virtual machine and run from there. You can then run the command line interface or use in python. Install with pip using::

    pip install epitopepredict

Or for latest version on github::

    pip install -e git+https://github.com/dmnfarrell/epitopepredict.git#egg=epitopepredict

**Python dependencies**

* numpy
* pandas
* matplotlib
* biopython
* tornado
* bokeh
* wtforms

Prediction algorithms
---------------------

There are now multiple MHC binding prediction algorithms available freely online. Often the problem is determining how to use them and which alleles they support. The 'state of the art' algorithms are probably those based on neural networks such as netMHC class I and II routines. These are packaged as external tools and can be installed freely on your system.

**Supported algorithms**

+---------------------+-------------------------------------------------------------+
| name                | description                                                 |
+=====================+=============================================================+
| basicmhc1           | built-in MHC-class I predictor                              |
+---------------------+-------------------------------------------------------------+
| tepitope            | implements the TEPITOPEPan method, built in (MHC-II)        |
+---------------------+-------------------------------------------------------------+
| netMHCpan           | http://www.cbs.dtu.dk/services/NetMHCpan/  (MHC-I)          |
+---------------------+-------------------------------------------------------------+
| netMHCIIpan         | http://www.cbs.dtu.dk/services/NetMHCIIpan/ (MHC-II)        |
+---------------------+-------------------------------------------------------------+
| mhcflurry           | https://github.com/openvax/mhcflurry (MHC-I)                |
+---------------------+-------------------------------------------------------------+
| IEDB MHC-I tools    | http://tools.immuneepitope.org/mhci/download/               |
+---------------------+-------------------------------------------------------------+

MHCFlurry can be easily installed easily with pip.

Installing netMHCpan and netMHCIIpan
------------------------------------

Due to license restrictions these programs must be installed separately. You can go to these respective links to fill in forms that will give you access to the install file:

 * http://www.cbs.dtu.dk/cgi-bin/nph-sw_request?netMHCpan
 * http://www.cbs.dtu.dk/cgi-bin/nph-sw_request?netMHCIIpan

The install instructions can then be found in the readme files when you untar the downloaded file e.g. netMHCpan-4.0.readme. Remember to test the software is working before you use it in epitopepredict.

Installing IEDB MHC-I tools
---------------------------

Note that if using the netMHCpan programs above you probably **DO NOT** need to use the IEDB tools unless you have specific requirements to do so. The distributions 'IEDB_MHC*.tar.gz' contain a collection of peptide binding prediction tools for Major Histocompatibility Complex (MHC) class I and II molecules. The collection is a mixture of pythons scripts and linux 32-bit environment specific binaries. Linux environment is required. Under ubuntu you should also install tcsh and gawk::

    sudo apt install tcsh gawk

Download from http://tools.iedb.org/mhci/download/. Unpack the tar.gz files. Run the 'configure' script to set up path variables for trained models. This has been tested to work with version 2.17.

::

    tar -zxvf IEDB_MHC_I-*.*.*.tar.gz
    cd mhc_i
    ./configure.py

*MHC-II tools are not currently supported.*

Submit Bugs
===========

This software is under active development particularly with a view to improve the command line tools. Please use the github project page to submit bugs or suggestions: http://dmnfarrell.github.io/epitopepredict

References
==========

* Zhang, L., Chen, Y., Wong, H.-S., Zhou, S., Mamitsuka, H., & Zhu, S. (2012). TEPITOPEpan: extending TEPITOPE for peptide binding prediction covering over 700 HLA-DR molecules. PloS One, 7(2), e30483. http://doi.org/10.1371/journal.pone.0030483

* Nielsen, M., Lund, O., Buus, S., & Lundegaard, C. (2010). MHC class II epitope predictive algorithms. Immunology, 130(3), 319–28. http://doi.org/10.1111/j.1365-2567.2010.03268.x

* Karosiene, E., Rasmussen, M., Blicher, T., Lund, O., Buus, S., & Nielsen, M. (2013). NetMHCIIpan-3.0, a common pan-specific MHC class II prediction method including all three human MHC class II isotypes, HLA-DR, HLA-DP and HLA-DQ. Immunogenetics, 65(10), 711–24. http://doi.org/10.1007/s00251-013-0720-y

* Chaves, F. a, Lee, A. H., Nayak, J. L., Richards, K. a, & Sant, A. J. (2012). The utility and limitations of current Web-available algorithms to predict peptides recognized by CD4 T cells in response to pathogen infection. Journal of Immunology (Baltimore, Md. : 1950), 188(9), 4235–48. http://doi.org/10.4049/jimmunol.1103640
