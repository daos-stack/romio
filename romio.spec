%if (0%{?suse_version} >= 1500)
%global romio_home %{_libdir}/mpi/gcc/mpich/romio
%else
%global romio_home %{_libdir}/mpich/romio
%endif


Name:       romio
Version:    4.0~a1
Release:    1%{?dist}
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
%if "%{?chroot_name}" == "opensuse-leap-15.1-x86_64" || "%{?chroot_name}" == "opensuse-leap-15.2-x86_64" || (0%{?suse_version} >= 1500 && 0%{?suse_version} < 1600)
%define distro leap15
%else
%define distro centos7
%endif
%endif
# TODO: need to figure out a way to get this from the Makefile when a PR-repos: is in use
Source0:    https://build.hpdd.intel.com/job/daos-stack/job/mpich/job/daos_adio-rpm/lastSuccessfulBuild/artifact/artifacts/%{distro}/%{name}-%{upstream_version}.tar.gz
Patch0:     packaged-runtests-%{distro}.patch

BuildRequires:  mpich-devel >= 3.4~a2-2%{?dist}
# this should be BR:ed by mpich-devel above
BuildRequires:  daos-devel
# this really should be Requires: by daos-devel
BuildRequires:  libuuid-devel
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
sed -i -e "s/\/builddir\/build\/BUILD\/mpich-%{upstream_version}\/src\/mpi\/romio/${PWD//\//\\/}/g" test/runtests test/Makefile


%build
cd test
make %{?_smp_mflags}


%install
cd test
%make_install
mkdir -p %{buildroot}%{romio_home}/test %{buildroot}%{_libdir}/romio
# create compatibility link
%if (0%{?suse_version} >= 1500)
ln -s ../mpi/gcc/mpich/romio/test %{buildroot}/%{_libdir}/romio/test
%else
ln -s ../mpich/romio/test %{buildroot}/%{_libdir}/romio/test
%endif

for p in runtests simple perf async coll_test coll_perf misc file_info excl    \
         large_array atomicity noncontig noncontig_coll i_noncontig split_coll \
         shared_fp large_file psimple status error noncontig_coll2             \
         aggregation1 aggregation2 async-multiple ordered_fp external32        \
         hindexed types_with_zeros darray_read syshints fperf fcoll_test fmisc \
         pfcoll_test test_hintfile ; do
    install -m 755 $p %{buildroot}%{romio_home}/test
done

# needed to upgrade a package with a /usr/lib64/romio/test dir to a symlink
%pretrans tests -p <lua>
-- Define the path to directory being replaced below.
-- DO NOT add a trailing slash at the end.
path = "/usr/lib64/romio"
st = posix.stat(path)
if st and st.type == "directory" then
  status = os.rename(path, path .. ".rpmmoved")
  if not status then
    suffix = 0
    while not status do
      suffix = suffix + 1
      status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
    end
    os.rename(path, path .. ".rpmmoved")
  end
end

%post tests
rm -rf %{_libdir}/romio.rpmmoved

%files tests
%{romio_home}
%{_libdir}/romio
%doc
%license

%changelog
* Mon May 31 2021 Brian J. Murrell <brian.murrell@intel.com> - 4.0~a1-1
- Build on EL8
- Remove the virtual provides
- Install under proper mpich prefix on all distros
- Create compatibility links on all distros
- Include pretrans scriptlet to handle the replacing of the previous dir
  with the compatibility symlink

* Wed Jan 20 2021 Kenneth Cain <kenneth.c.cain@intel.com> - 3.4~a2-1
- Update packaging to build with libdaos.so.1

* Tue Jan 21 2020 Brian J. Murrell <brian.murrell@intel.com> - 3.3-3
- Add Leap 15.1 support

* Sun Dec 29 2019 Brian J. Murrell <brian.murrell@intel.com> - 3.3-2
- Add Provides: %{name}-cart-%{cart_major}-daos-%{daos_major}

* Tue Sep 03 2019 Brian J. Murrell <brian.murrell@intel.com> - 3.3-1
- Initial package
- Temporarily BR: daos-devel, until mercury-devel R:s it
