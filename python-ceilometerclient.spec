%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:             python-ceilometerclient
Version:          2.3.0
Release:          1%{?dist}
Summary:          Python API and CLI for OpenStack Ceilometer

License:          ASL 2.0
URL:              https://github.com/openstack/%{name}
Source0:          https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}%{?milestone}.tar.gz

BuildArch:        noarch
BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-pbr
BuildRequires:    python-d2to1

Requires:         python-setuptools
Requires:         python-argparse
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

%description
This is a client library for Ceilometer built on the Ceilometer API. It
provides a Python API (the ceilometerclient module) and a command-line tool
(ceilometer).


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

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# Fix hidden-file-or-dir warnings
rm -rf html/.doctrees html/.buildinfo

%files
%doc README.rst
%license LICENSE
%{_bindir}/ceilometer
%{python2_sitelib}/ceilometerclient
%{python2_sitelib}/*.egg-info

%files doc
%doc html

%changelog
* Wed Mar 23 2016 RDO <rdo-list@redhat.com> 2.3.0-0.1
 -  Rebuild for Mitaka 
