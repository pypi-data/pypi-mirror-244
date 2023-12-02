# SPDX-FileCopyrightText: 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT
# License text: https://spdx.org/licenses/MIT

Name:           python-sourcehutx
Version:        0.2.0
Release:        1%{?dist}
Summary:        Async Python client for the Sourcehut API

License:        MIT
URL:            https://sr.ht/~gotmax23/sourcehutx
%global furl    https://git.sr.ht/~gotmax23/sourcehutx
Source0:        %{furl}/refs/download/v%{version}/sourcehutx-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  gnupg2
BuildRequires:  python3-devel

%global _description %{expand:
This library provides an async python client for the Sourcehut API
implemented using httpx and pydantic.}

%description %_description

%package -n python3-sourcehutx
Summary:        %{summary}

%description -n python3-sourcehutx %_description


%prep
%autosetup -p1 -n sourcehutx-%{version}


%generate_buildrequires
%pyproject_buildrequires -x test


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files sourcehut


%check
%pytest


%files -n python3-sourcehutx -f %{pyproject_files}
%doc README.md NEWS.md
%license LICENSES/*


%changelog

* Sat Dec 2 2023 Maxwell G <maxwell@gtmx.me> - 0.2.0-1
- Release 0.2.0.

* Sun Aug 27 2023 Maxwell G <maxwell@gtmx.me> - 0.1.0-1
- Release 0.1.0.

* Sat Aug 26 2023 Maxwell G <maxwell@gtmx.me> - 0.0.2-1
- Release 0.0.2.

* Sat Aug 26 2023 Maxwell G <maxwell@gtmx.me> - 0.0.1-1
- Release 0.0.1.
