Name:      lava-test-plans
Version:   3.2.0
Release:   0%{?dist}
Summary:   The lava-test-plans project makes it easier to generate LAVA job.
License:   MIT
URL:       https://github.com/linaro/lava-test-plans
Source0:   %{pypi_source}


BuildRequires: git
BuildRequires: make
BuildRequires: python3-devel
BuildRequires: python3-flit
BuildRequires: python3-pip
BuildRequires: python3-pytest
BuildRequires: python3-pytest-cov
BuildRequires: python3-pytest-mock
BuildRequires: python3-configobj
BuildRequires: python3-docker
BuildRequires: python3-jinja2
BuildRequires: python3-requests == 2.31
BuildRequires: python3-ruamel-yaml

BuildArch: noarch

Requires: python3 >= 3.6
Requires: python3-configobj
Requires: python3-docker
Requires: python3-jinja2
Requires: python3-requests == 2.31
Requires: python3-ruamel-yaml

%global debug_package %{nil}

%description
The lava-test-plans project makes it easier to generate LAVA job.
It generates the LAVA job definition file from a set of templates.

%prep
%setup -q

%build
export FLIT_NO_NETWORK=1
make run
#make man
#make bash_completion

%check
export SKIP_TEST_LAVA_VALIDITY=1
python3 -m pytest test/

%install
mkdir -p %{buildroot}/usr/share/%{name}/
cp -r run %{dist} %{buildroot}/usr/share/%{name}/
mkdir -p %{buildroot}/usr/bin
ln -sf ../share/%{name}/run %{buildroot}/usr/bin/%{name}
#mkdir -p %{buildroot}%{_mandir}/man1
#install -m 644 %{name}.1 %{buildroot}%{_mandir}/man1/
#mkdir -p %{buildroot}/usr/share/bash-completion/completions/
#install -m 644 bash_completion/%{name} %{buildroot}/usr/share/bash-completion/completions/

%files
/usr/share/%{name}
%{_bindir}/%{name}
#%{_mandir}/man1/%{name}.1*
#/usr/share/bash-completion/completions/%{name}

%doc README.md
%license LICENSE

%changelog

* Tue Sep 06 2022 Anders Roxell <anders.roxell@linaro.org> - 3.0-1
- Initial version of the package
