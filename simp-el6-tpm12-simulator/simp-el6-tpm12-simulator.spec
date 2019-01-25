Name: simp-el6-tpm12-simulator
Version: 4769.0.0
Release: 0%{?dist}
Summary: The IBM TPM1.2 simulator

# SIMP customization:
%global _prefix /usr/local
%global _name tpm12-simulator

License: BSD
URL:     https://sourceforge.net/projects/ibmswtpm/
###https://sourceforge.net/projects/ibmswtpm/files/tpm4769tar.gz/download
###https://sourceforge.net/projects/ibmswtpm/files/tpm%%{version}tar.gz/download
Source0: %{name}-%{version}.tar.gz
Source1: %{name}
Source2: %{name}.environment
Source3: simp-el6-tpm12-tpmbios
Source4: simp-el6-tpm12-tpminit
Source5: simp-el6-tpm12-tcsd
Source6: tpminit

BuildRequires: gcc
BuildRequires: openssl-devel
BuildRequires: libtool

%description
IBM's Software Trusted Platform Module (TPM) includes a TPM 1.2 implementation,
low level demo libraries and command line tools, a TPM test suite, and proxies
to connect from a TCP/IP socket to a hardware TPM.

This version has been packaged by the SIMP team for %{dist}

%prep
%setup -q %{SOURCE0}

%build
cd tpm/
mkdir src
make -f makefile-tpm
cd ../libtpm
./autogen
./configure
make
#%make_build

%install
install -m 0755 -D tpm/tpm_server %{buildroot}%{_bindir}/%{_name}
install -m 0755 -D libtpm/utils/tpmbios %{buildroot}%{_bindir}/tpmbios
install -m 0755 -D libtpm/utils/createek %{buildroot}%{_bindir}/createek
install -m 0755 -D libtpm/utils/nv_definespace %{buildroot}%{_bindir}/nv_definespace
install -m 0755 -D %{SOURCE6}     %{buildroot}%{_bindir}/tpminit
install -m 0755 -D %{SOURCE1}     %{buildroot}%{_initddir}/%{_name}
install -m 0644 -D %{SOURCE2}     %{buildroot}%{_sysconfdir}/default/%{_name}
install -m 0755 -D %{SOURCE3}     %{buildroot}%{_initddir}/tpm12-tpmbios
install -m 0755 -D %{SOURCE4}     %{buildroot}%{_initddir}/tpm12-tpminit
install -m 0755 -D %{SOURCE5}     %{buildroot}%{_initddir}/tpm12-tcsd

%files
%{_bindir}/%{_name}
%{_bindir}/tpmbios
%{_bindir}/createek
%{_bindir}/nv_definespace
%{_bindir}/tpminit
%{_initddir}/%{_name}
%{_sysconfdir}/default/%{_name}
%{_initddir}/tpm12-tpmbios
%{_initddir}/tpm12-tpminit
%{_initddir}/tpm12-tcsd


%pre
mkdir -p %{_datadir}

getent group tss >/dev/null || groupadd -g 62 -r tss
getent passwd tss >/dev/null || \
useradd -r -u 59 -g tss -d /dev/null -s /sbin/nologin \
 -c "Account used by the trousers package to sandbox the tcsd daemon" tss
exit 0

%post
%systemd_postun %{_name}
%systemd_postun simp-el6-tpm12-tpmbios
%systemd_postun simp-el6-tpm12-tpminit
%systemd_postun simp-el6-tpm12-tcsd

%preun
%systemd_preun %{_name}
%systemd_preun simp-el6-tpm12-tpmbios
%systemd_postun simp-el6-tpm12-tpminit
%systemd_postun simp-el6-tpm12-tcsd

%postun
%systemd_postun %{_name}
%systemd_postun simp-el6-tpm12-tpmbios
%systemd_postun simp-el6-tpm12-tpminit
%systemd_postun simp-el6-tpm12-tcsd

%changelog
* Fri Jan 25 2019 Michael Morrone <michael.morrone@onyxpoint.com> - 0.0.1
- Initial commit
