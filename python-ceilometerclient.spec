%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

%global sname ceilometerclient
%global sum Python API and CLI for OpenStack Ceilometer

Name:             python-ceilometerclient
Version:          XXX
Release:          XXX
Summary:          %{sum}

License:          ASL 2.0
URL:              https://github.com/openstack/%{name}
Source0:          http://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:        noarch

BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-pbr >= 1.6
BuildRequires:    python-keystoneclient
%if 0%{?with_python3}
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr >= 1.6
BuildRequires:    python3-keystoneclient
%endif

%description
This is a client library for Ceilometer built on the Ceilometer API. It
provides a Python API (the ceilometerclient module) and a command-line tool
(ceilometer).


%package -n python2-%{sname}
Summary:          %{sum}
# from requirements.txt
Requires:         python-iso8601
Requires:         python-oslo-i18n
Requires:         python-oslo-serialization
Requires:         python-oslo-utils
Requires:         python-keystoneclient
Requires:         python-requests >= 2.5.2
Requires:         python-six >= 1.9.0
Requires:         python-stevedore
Requires:         python-pbr >= 1.6
%{?python_provide:%python_provide python2-%{sname}}

%description -n python2-%{sname}
This is a client library for Ceilometer built on the Ceilometer API. It
provides a Python API (the ceilometerclient module) and a command-line tool
(ceilometer).


%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:          %{sum}
# from requirements.txt
Requires:         python3-iso8601
Requires:         python3-oslo-i18n
Requires:         python3-oslo-serialization
Requires:         python3-oslo-utils
Requires:         python3-keystoneclient
Requires:         python3-requests >= 2.5.2
Requires:         python3-six >= 1.9.0
Requires:         python3-stevedore
Requires:         python3-pbr >= 1.6
%{?python_provide:%python_provide python3-%{sname}}

%description -n python3-%{sname}
This is a client library for Ceilometer built on the Ceilometer API. It
provides a Python API (the ceilometerclient module) and a command-line tool
(ceilometer).
%endif # with_python3


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
rm -rf python_%{sname}.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

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

# Build HTML docs
export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# Fix hidden-file-or-dir warnings
rm -rf html/.doctrees html/.buildinfo

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
%{python2_sitelib}/*.egg-info
%{_bindir}/ceilometer-3
%{_bindir}/ceilometer-%{python3_version}
%endif # with_python3

%files doc
%license LICENSE
%doc html

%changelog
