%global romio_home %{_libdir}/romio

Name:       romio
Version:    3.3
Release:    1%{?dist}
Summary:    ROMIO

License:    MIT
URL:        http://www.mpich.org/
Source0:    https://build.hpdd.intel.com/job/daos-stack/job/mpich/job/daos_adio-rpm/lastSuccessfulBuild/artifact/artifacts/%{name}-%{version}.tar.gz
Patch0:     packaged-runtests.patch

BuildRequires:  mpich-devel
# this should be BR:ed by mpich-devel above
BuildRequires:  daos-devel

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
* Tue Sep 03 2019 Brian J. Murrell <brian.murrell@intel.com> - 3.3-1
- Initial package
- Temporarily BR: daos-devel, until mercury-devel R:s it