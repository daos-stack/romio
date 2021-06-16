NAME             := romio
SRC_EXT          := gz
TEST_PACKAGES    := romio-tests

include packaging/Makefile_packaging.mk

# need to force rebuilding the SRPM because the source tarball is
# distro specific
romio-$(DL_VERSION).tar.gz: FORCE

$(SRPM): FORCE