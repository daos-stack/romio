NAME             := romio
SRC_EXT          := gz
TEST_PACKAGES    := romio-tests

include packaging/Makefile_packaging.mk

# PR-repos* support for the Source: in the specfile
MPICH_REPO := $(shell echo " $($(DISTRO_BASE)_PR_REPOS) $(PR_REPOS) " | sed -ne 's/ \(mpich@[^ ]*\) .*/ \1 /' -e 's/^.* mpich@\([^ ]*\) .*$$/\1/p')
ifeq ($(findstring :,$(MPICH_REPO)),:)
MPICH_REPO := $(subst :, ,$(MPICH_REPO))
endif
BUILD_JOB  := $(word 1, $(MPICH_REPO))
ifneq ($(BUILD_JOB),)
BUILD_DEFINES := --define "buildjob $(BUILD_JOB)"
endif
BUILD_NUM  := $(word 2, $(MPICH_REPO))
ifneq ($(BUILD_NUM),)
BUILD_DEFINES += --define "buildnum $(BUILD_NUM)"
endif

# need to force rebuilding the SRPM because the source tarball is
# distro specific
romio-$(DL_VERSION).tar.gz: FORCE

$(SRPM): FORCE