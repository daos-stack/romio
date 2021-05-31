%global romio_home %{_libdir}/romio

Name:       romio
Version:    3.4~a2
Release:    2%{?dist}
Summary:    ROMIO

License:    MIT
URL:        http://www.mpich.org/

# upstream_version is version with ~ removed
%{lua:
    rpm.define("upstream_version " .. string.gsub(rpm.expand("%{version}"), "~", ""))
}

%{!?chroot_name: %define chroot_name %{getenv:CHROOT_NAME}}

%if "%{?chroot_name}" == "epel-8-x86_64" || "%{?rhel}" == "8"
%define distro centos8
%else
%if "%{?chroot_name}" == "opensuse-leap-15.1-x86_64" || "%{?chroot_name}" == "opensuse-leap-15.2-x86_64" || (0%{?suse_version} >= 1500) && (0%{?suse_version} < 1600)
%define distro leap15
%else
%define distro centos7
%endif
%endif
%endif
# TODO: need to figure out a way to get this from the Makefile
#Source0:    https://build.hpdd.intel.com/job/daos-stack/job/mpich/job/daos_adio-rpm/lastSuccessfulBuild/artifact/artifacts/%{distro}/%{name}-%{upstream_version}.tar.gz
Source0:    https://build.hpdd.intel.com/job/daos-stack/job/mpich/view/change-requests/job/PR-47/lastSuccessfulBuild/artifact/artifacts/%{distro}/%{name}-%{upstream_version}.tar.gz
Patch0:     packaged-runtests-%{distro}.patch

BuildRequires:  mpich-devel >= 3.4~a2-2%{?dist}
# this should be BR:ed by mpich-devel above
BuildRequires:  daos-devel
%if (0%{?suse_version} >= 1500)
BuildRequires:  gcc-fortran
%endif

%description
ROMIO

%package tests
Summary:    ROMIO tests

%description tests
ROMIO tests

%prep
%autosetup -n romio -p1
sed -i -e "s/\/builddir\/build\/BUILD\/mpich-%{version}\/src\/mpi\/romio/${PWD//\//\\/}/g" test/runtests test/Makefile


%build
cd test
make %{?_smp_mflags}


%install
cd test
%make_install
mkdir -p %{buildroot}%{romio_home}/test
for p in runtests simple perf async coll_test coll_perf misc file_info excl    \
         large_array atomicity noncontig noncontig_coll i_noncontig split_coll \
         shared_fp large_file psimple status error noncontig_coll2             \
         aggregation1 aggregation2 async-multiple ordered_fp external32        \
         hindexed types_with_zeros darray_read syshints fperf fcoll_test fmisc \
         pfcoll_test test_hintfile ; do
    install -m 755 $p %{buildroot}%{romio_home}/test
done

%files tests
%{romio_home}
%doc
%license

%changelog
* Mon May 31 2021 Brian J. Murrell <brian.murrell@intel.com> - 3.4~a2-2
- Build on EL8
- Remove the virtual provides

* Wed Jan 20 2021 Kenneth Cain <kenneth.c.cain@intel.com> - 3.4~a2-1
- Update packaging to build with libdaos.so.1

* Tue Jan 21 2020 Brian J. Murrell <brian.murrell@intel.com> - 3.3-3
- Add Leap 15.1 support

* Sun Dec 29 2019 Brian J. Murrell <brian.murrell@intel.com> - 3.3-2
- Add Provides: %{name}-cart-%{cart_major}-daos-%{daos_major}

* Tue Sep 03 2019 Brian J. Murrell <brian.murrell@intel.com> - 3.3-1
- Initial package
- Temporarily BR: daos-devel, until mercury-devel R:s it
