# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname ceilometerclient
%global sum Python API and CLI for OpenStack Ceilometer

# oslosphinx do not work with sphinx > 2
%global with_doc 0

%global common_desc \
This is a client library for Ceilometer built on the Ceilometer API. It \
provides a Python API (the ceilometerclient module) and a command-line tool \
(ceilometer).

Name:             python-ceilometerclient
Version:          XXX
Release:          XXX
Summary:          %{sum}

License:          ASL 2.0
URL:              https://github.com/openstack/%{name}
Source0:          https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:        noarch

BuildRequires:    git
BuildRequires:    openstack-macros
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-pbr >= 1.6

%description
%{common_desc}

%package -n python%{pyver}-%{sname}
Summary:          %{sum}
%{?python_provide:%python_provide python%{pyver}-%{sname}}
%if %{pyver} == 3
Obsoletes: python2-%{sname} < %{version}-%{release}
%endif

# from requirements.txt
Requires:         python%{pyver}-iso8601
Requires:         python%{pyver}-oslo-i18n >= 2.1.0
Requires:         python%{pyver}-oslo-serialization >= 1.10.0
Requires:         python%{pyver}-oslo-utils >= 3.17.0
Requires:         python%{pyver}-requests >= 2.8.1
Requires:         python%{pyver}-six >= 1.9.0
Requires:         python%{pyver}-stevedore
Requires:         python%{pyver}-pbr
Requires:         python%{pyver}-keystoneauth1 >= 2.1.0
Requires:         python%{pyver}-prettytable

%description -n python%{pyver}-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Ceilometer API Client

BuildRequires:    python%{pyver}-sphinx
# FIXME: remove following line when a new release including https://review.openstack.org/#/c/476759/ is in u-u
BuildRequires:    python%{pyver}-oslo-sphinx
BuildRequires:    python%{pyver}-openstackdocstheme

%description      doc
%{common_desc}
%endif

This package contains auto-generated documentation.


%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf python_%{sname}.egg-info

# Let RPM handle the requirements
%py_req_cleanup

%build
%{pyver_build}

%if 0%{?with_doc}
%if %{pyver} == 3
# 'execfile' is not available in python3
sed -i 's/execfile(os.path.join("..", "ext", "gen_ref.py"))/exec(open(os.path.join("..", "ext", "gen_ref.py")).read())/' doc/source/conf.py
%endif

# Build HTML docs
%{pyver_bin} setup.py build_sphinx -b html

# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%install
%{pyver_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s ceilometer %{buildroot}%{_bindir}/ceilometer-%{pyver}

# Delete tests
rm -fr %{buildroot}%{pyver_sitelib}/%{sname}/tests

%files -n python%{pyver}-%{sname}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{sname}
%{pyver_sitelib}/*.egg-info
%{_bindir}/ceilometer
%{_bindir}/ceilometer-%{pyver}

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
