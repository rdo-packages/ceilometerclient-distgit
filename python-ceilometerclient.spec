%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname ceilometerclient

%if 0%{?fedora}
%global with_python3 1
%endif

Name:             python-ceilometerclient
Version:          XXX
Release:          XXX
Summary:          Python API and CLI for OpenStack Ceilometer

License:          ASL 2.0
URL:              https://bugs.launchpad.net/python-ceilometerclient
Source0:          http://tarballs.openstack.org/python-ceilometerclient/%{name}/%{name}-%{version}.tar.gz

BuildArch:        noarch

%description
This is a client library for Ceilometer built on the Ceilometer API. It
provides a Python API (the ceilometerclient module) and a command-line tool
(ceilometer).

%package -n python2-%{sname}
Summary:          Python API and CLI for OpenStack Ceilometer
%{?python_provide:%python_provide python2-ceilometerclient}

BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-pbr

Requires:         python-setuptools
Requires:         python-prettytable
Requires:         python-iso8601
Requires:         python-oslo-i18n
Requires:         python-oslo-serialization
Requires:         python-oslo-utils
Requires:         python-keystoneclient
Requires:         python-requests >= 2.5.2
Requires:         python-six >= 1.9.0
Requires:         python-stevedore
Requires:         python-pbr

%description -n python2-%{sname}
This is a client library for Ceilometer built on the Ceilometer API. It
provides a Python API (the ceilometerclient module) and a command-line tool
(ceilometer).

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:          Python API and CLI for OpenStack Ceilometer
%{?python_provide:%python_provide python3-ceilometerclient}

BuildRequires:    python3-setuptools
BuildRequires:    python3-devel
BuildRequires:    python3-pbr

Requires:         python3-setuptools
Requires:         python3-prettytable
Requires:         python3-iso8601
Requires:         python3-oslo-i18n
Requires:         python3-oslo-serialization
Requires:         python3-oslo-utils
Requires:         python3-keystoneclient
Requires:         python3-requests >= 2.5.2
Requires:         python3-six >= 1.9.0
Requires:         python3-stevedore
Requires:         python3-pbr

%description -n python3-%{sname}
This is a client library for Ceilometer built on the Ceilometer API. It
provides a Python API (the ceilometerclient module) and a command-line tool
(ceilometer).
%endif

%package doc
Summary:          Documentation for OpenStack Ceilometer API Client

BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx

%description      doc
This is a client library for Ceilometer built on the Ceilometer API. It
provides a Python API (the ceilometerclient module) and a command-line tool
(ceilometer).

This package contains auto-generated documentation.

%prep
%setup -q -n %{name}-%{upstream_version}

# Remove bundled egg-info
rm -rf python_ceilometerclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/ceilometer %{buildroot}%{_bindir}/ceilometer-%{python3_version}
ln -s ./ceilometer-%{python3_version} %{buildroot}%{_bindir}/ceilometer-3
# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/ceilometerclient/tests
%endif

%py2_install
mv %{buildroot}%{_bindir}/ceilometer %{buildroot}%{_bindir}/ceilometer-%{python2_version}
ln -s ./ceilometer-%{python2_version} %{buildroot}%{_bindir}/ceilometer-2

ln -s ./ceilometer-2 %{buildroot}%{_bindir}/ceilometer

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/ceilometerclient/tests


export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/ceilometerclient
%{python2_sitelib}/*.egg-info
%{_bindir}/ceilometer
%{_bindir}/ceilometer-2
%{_bindir}/ceilometer-%{python2_version}

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/ceilometerclient
%{python3_sitelib}/*.egg-info
%{_bindir}/ceilometer-3
%{_bindir}/ceilometer-%{python3_version}
%endif

%files doc
%doc html
%license LICENSE

%changelog
