%global romio_home %{_libdir}/romio
%global cart_major 4
%global daos_major 0

Name:       romio
Version:    3.3
Release:    3%{?dist}
Summary:    ROMIO

License:    MIT
URL:        http://www.mpich.org/

%{!?chroot_name: %define chroot_name %{getenv:CHROOT_NAME}}

%if ("%{?chroot_name}" == "epel-7-x86_64")
%define distro centos7
%else
%if ("%{?chroot_name}" == "opensuse-leap-15.1-x86_64")
%define distro leap15
%else
%if (0%{?suse_version} >= 1500) && (0%{?suse_version} < 1600)
%define distro leap15
%else
%define distro centos7
%endif
%endif
%endif
Source0:    https://build.hpdd.intel.com/job/daos-stack/job/mpich/job/PR-24/lastSuccessfulBuild/artifact/artifacts/%{distro}/%{name}-%{version}.tar.gz
Patch0:     packaged-runtests-%{distro}.patch

BuildRequires:  mpich-devel
# this should be BR:ed by mpich-devel above
BuildRequires:  daos-devel
%if (0%{?suse_version} >= 1500)
BuildRequires:  gcc-fortran
%endif
Provides:       %{name}-cart-%{cart_major}-daos-%{daos_major}

%description
ROMIO

%package tests
Summary:    ROMIO tests
Provides:       %{name}-tests-cart-%{cart_major}-daos-%{daos_major}

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
* Tue Jan 21 2020 Brian J. Murrell <brian.murrell@intel.com> - 3.3-3
- Add Leap 15.1 support

* Sun Dec 29 2019 Brian J. Murrell <brian.murrell@intel.com> - 3.3-2
- Add Provides: %{name}-cart-%{cart_major}-daos-%{daos_major}

* Tue Sep 03 2019 Brian J. Murrell <brian.murrell@intel.com> - 3.3-1
- Initial package
- Temporarily BR: daos-devel, until mercury-devel R:s it
