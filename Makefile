NAME             := romio
SRC_EXT          := gz
TEST_PACKAGES    := romio-tests

include packaging/Makefile_packaging.mk

# need to force rebuilding the SRPM because the source tarball is
# distro specific
romio-3.4a2.tar.gz: FORCE

$(SRPM): FORCE