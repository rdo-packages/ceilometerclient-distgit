Name:             python-ceilometerclient
Version:          1.5.0
Release:          1%{?dist}
Summary:          Python API and CLI for OpenStack Ceilometer

Group:            Development/Languages
License:          ASL 2.0
URL:              https://github.com/openstack/%{name}
Source0:          https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:        noarch
BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-pbr
BuildRequires:    python-d2to1

Requires:         python-setuptools
Requires:         python-argparse
Requires:         python-prettytable
Requires:         python-iso8601
Requires:         python-oslo-i18n >= 1.5.0
Requires:         python-oslo-serialization >= 1.4.0
Requires:         python-oslo-utils >= 2.0.0
Requires:         python-keystoneclient >= 1.6.0
Requires:         python-six >= 1.7.0
Requires:         python-stevedore >= 1.5.0
Requires:         python-requests >= 2.5.2
Requires:         python-pbr


%description
This is a client library for Ceilometer built on the Ceilometer API. It
provides a Python API (the ceilometerclient module) and a command-line tool
(ceilometer).


%package doc
Summary:          Documentation for OpenStack Ceilometer API Client
Group:            Documentation

BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx >= 2.5.0

%description      doc
This is a client library for Ceilometer built on the Ceilometer API. It
provides a Python API (the ceilometerclient module) and a command-line tool
(ceilometer).

This package contains auto-generated documentation.


%prep
%setup -q

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# Fix hidden-file-or-dir warnings
rm -rf html/.doctrees html/.buildinfo

%files
%license LICENSE
%doc README.rst
%{_bindir}/ceilometer
%{python_sitelib}/ceilometerclient
%{python_sitelib}/*.egg-info

%files doc
%license LICENSE
%doc html

%changelog
* Thu Sep 17 2015 Haikel Guemar <hguemar@fedoraproject.org> 1.5.0-1
- Update to upstream 1.5.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 20 2015 Alan Pevec <alan.pevec@redhat.com> 1.0.13-1
- Update to upstream 1.0.13

* Wed Oct 08 2014 Jakub Ruzicka <jruzicka@redhat.com> 1.0.12-1
- Update to upstream 1.0.12
- New Requires: python-oslo-utils
- New doc BuildRequires: python-oslo-utils
- oslosphinx -> oslo.sphinx fix

* Tue Sep 23 2014 Jakub Ruzicka <jruzicka@redhat.com> 1.0.11-1
- Update to upstream 1.0.11
- New Requires: python-stevedore

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun 05 2014 Jakub Ruzicka <jruzicka@redhat.com> 1.0.10-1
- Update to upstream 1.0.10
- Remove requirements.txt in .spec instead of patch

* Mon Feb 17 2014 Pádraig Brady <pbrady@redhat.com> - 1.0.9-3
- Require python-six >= 1.4.1 to ensure update

* Mon Feb 17 2014 Alan Pevec <apevec@redhat.com> 1.0.9-1
- Update to upstream 1.0.9

* Mon Dec 16 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.8-1
- Update to upstream 1.0.8
- New dependency: python-six

* Mon Oct 07 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.6-1
- Update to upstream 1.0.6.

* Mon Sep 09 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.3-1
- Update to upstream 1.0.3.
- README extension changed.
- Get rid of pbr deps in the patch instead of this spec file.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.1-2
- New build requires: python-d2to1, python-pbr.

* Tue Jul 16 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.1-1
- Update to upstream version 1.0.1.
- Remove new runtime dependency on python-pbr.
- Remove requirements file.
- Make requires generic instead of requiring specific versions.

* Mon Apr 01 2013 Jakub Ruzicka <jruzicka@redhat.com> 1.0.0
- Update to upstream version 1.0.0.
- Added Requires: python-keystoneclient >= 0.1.2.

* Tue Mar 26 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.0.10-0.2.gitd84fd99
- Add BuildRequires: python2-devel.

* Tue Mar 26 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.0.10-0.1.gitd84fd99
- Initial package based on python-novaclient.
