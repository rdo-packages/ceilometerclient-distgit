%if 0%{?fedora}
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:             python-ceilometerclient
Version:          XXX
Release:          XXX
Summary:          Python API and CLI for OpenStack Ceilometer

License:          ASL 2.0
URL:              https://github.com/openstack/%{name}
Source0:          https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

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

Requires:         python-iso8601
Requires:         python-oslo-i18n
Requires:         python-oslo-serialization
Requires:         python-oslo-utils
Requires:         python-keystoneclient
Requires:         python-requests >= 2.5.2
Requires:         python-six >= 1.9.0
Requires:         python-stevedore
Requires:         python-pbr

%description
This is a client library for Ceilometer built on the Ceilometer API. It
provides a Python API (the ceilometerclient module) and a command-line tool
(ceilometer).

%if 0%{?with_python3}
%package -n python3-ceilometerclient
Summary:    Client library for OpenStack Identity API
# from requirements.txt
Requires:         python3-iso8601
Requires:         python3-oslo-i18n
Requires:         python3-oslo-serialization
Requires:         python3-oslo-utils
Requires:         python3-keystoneclient
Requires:         python3-requests >= 2.5.2
Requires:         python3-six >= 1.9.0
Requires:         python3-stevedore
Requires:         python3-pbr

%description -n python3-ceilometerclient
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
rm -rf python_ceilometerclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%{__python2} setup.py build
%if 0%{?with_python3}
%{__python3} setup.py build
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%if 0%{?with_python3}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
%endif

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/tests
%if 0%{?with_python3}
rm -fr %{buildroot}%{python3_sitelib}/tests
%endif

# Build HTML docs
export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# Fix hidden-file-or-dir warnings
rm -rf html/.doctrees html/.buildinfo

%files
%doc README.rst
%license LICENSE
%{python2_sitelib}/*
%{_bindir}/ceilometer

%if 0%{?with_python3}
%files -n python3-ceilometerclient
%doc README.rst
%license LICENSE
%{python3_sitelib}/*
%endif # with_python3

%files doc
%doc html
%license LICENSE

%changelog
