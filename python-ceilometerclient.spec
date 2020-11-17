%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:        noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:    git-core
BuildRequires:    openstack-macros
BuildRequires:    python3-setuptools
BuildRequires:    python3-devel
BuildRequires:    python3-pbr >= 1.6

%description
%{common_desc}

%package -n python3-%{sname}
Summary:          %{sum}
%{?python_provide:%python_provide python3-%{sname}}
Obsoletes: python2-%{sname} < %{version}-%{release}

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

%description -n python3-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Ceilometer API Client

BuildRequires:    python3-sphinx
# FIXME: remove following line when a new release including https://review.openstack.org/#/c/476759/ is in u-u
BuildRequires:    python3-oslo-sphinx
BuildRequires:    python3-openstackdocstheme

%description      doc
%{common_desc}
%endif

This package contains auto-generated documentation.


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf python_%{sname}.egg-info

# Let RPM handle the requirements
%py_req_cleanup

%build
%{py3_build}

%if 0%{?with_doc}
# 'execfile' is not available in python3
sed -i 's/execfile(os.path.join("..", "ext", "gen_ref.py"))/exec(open(os.path.join("..", "ext", "gen_ref.py")).read())/' doc/source/conf.py

# Build HTML docs
%{__python3} setup.py build_sphinx -b html

# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%install
%{py3_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s ceilometer %{buildroot}%{_bindir}/ceilometer-3

# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/%{sname}/tests

%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_bindir}/ceilometer
%{_bindir}/ceilometer-3

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
