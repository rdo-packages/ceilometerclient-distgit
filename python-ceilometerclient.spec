%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

%global sname ceilometerclient
%global sum Python API and CLI for OpenStack Ceilometer

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
BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-pbr >= 1.6
%if 0%{?with_python3}
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr >= 1.6
%endif

%description
%{common_desc}

%package -n python2-%{sname}
Summary:          %{sum}
# from requirements.txt
Requires:         python-iso8601
Requires:         python-oslo-i18n >= 2.1.0
Requires:         python-oslo-serialization >= 1.10.0
Requires:         python-oslo-utils >= 3.17.0
Requires:         python-requests >= 2.8.1
Requires:         python-six >= 1.9.0
Requires:         python-stevedore
Requires:         python-pbr
Requires:         python-keystoneauth1 >= 2.1.0
Requires:         python-prettytable
%{?python_provide:%python_provide python2-%{sname}}

%description -n python2-%{sname}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:          %{sum}
# from requirements.txt
Requires:         python3-iso8601
Requires:         python3-oslo-i18n >= 2.1.0
Requires:         python3-oslo-serialization >= 1.10.0
Requires:         python3-oslo-utils >= 3.17.0
Requires:         python3-requests >= 2.8.1
Requires:         python3-six >= 1.9.0
Requires:         python3-stevedore
Requires:         python3-pbr
Requires:         python3-keystoneauth1 >= 2.1.0
Requires:         python3-prettytable
%{?python_provide:%python_provide python3-%{sname}}

%description -n python3-%{sname}
%{common_desc}
%endif # with_python3


%package doc
Summary:          Documentation for OpenStack Ceilometer API Client

BuildRequires:    python-sphinx
# FIXME: remove following line when a new release including https://review.openstack.org/#/c/476759/ is in u-u
BuildRequires:    python-oslo-sphinx
BuildRequires:    python-openstackdocstheme

%description      doc
%{common_desc}

This package contains auto-generated documentation.


%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf python_%{sname}.egg-info

# Let RPM handle the requirements
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# Build HTML docs
%{__python2} setup.py build_sphinx -b html

# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.doctrees doc/build/html/.buildinfo

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%if 0%{?with_python3}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
%endif

%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/ceilometer %{buildroot}%{_bindir}/ceilometer-%{python3_version}
ln -s ./ceilometer-%{python3_version} %{buildroot}%{_bindir}/ceilometer-3
%endif

%py2_install
mv %{buildroot}%{_bindir}/ceilometer %{buildroot}%{_bindir}/ceilometer-%{python2_version}
ln -s ./ceilometer-%{python2_version} %{buildroot}%{_bindir}/ceilometer-2

ln -s ./ceilometer-2 %{buildroot}%{_bindir}/ceilometer

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/%{sname}/tests
%if 0%{?with_python3}
rm -fr %{buildroot}%{python3_sitelib}/%{sname}/tests
%endif

%files -n python2-%{sname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{sname}
%{python2_sitelib}/*.egg-info
%{_bindir}/ceilometer
%{_bindir}/ceilometer-2
%{_bindir}/ceilometer-%{python2_version}

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_bindir}/ceilometer-3
%{_bindir}/ceilometer-%{python3_version}
%endif # with_python3

%files doc
%license LICENSE
%doc doc/build/html

%changelog
