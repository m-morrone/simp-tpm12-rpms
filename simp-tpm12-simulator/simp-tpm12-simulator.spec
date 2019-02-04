Name: simp-tpm12-simulator
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
Source1: %{name}.service
Source2: %{name}.environment
Source3: simp-tpm12-tpmbios.service
Source4: simp-tpm12-tpminit.service
Source5: simp-tpm12-tcsd.service
Source6: tpminit
Source7: tcsdstarter

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
install -m 0755 -D %{SOURCE7}     %{buildroot}%{_bindir}/tcsdstarter
install -m 0644 -D %{SOURCE1}     %{buildroot}%{_unitdir}/%{_name}.service
install -m 0644 -D %{SOURCE2}     %{buildroot}%{_sysconfdir}/default/%{_name}
install -m 0644 -D %{SOURCE3}     %{buildroot}%{_unitdir}/tpm12-tpmbios.service
install -m 0644 -D %{SOURCE4}     %{buildroot}%{_unitdir}/tpm12-tpminit.service
install -m 0644 -D %{SOURCE5}     %{buildroot}%{_unitdir}/tpm12-tcsd.service

%files
%license LICENSE
%{_bindir}/%{_name}
%{_bindir}/tpmbios
%{_bindir}/createek
%{_bindir}/nv_definespace
%{_bindir}/tpminit
%{_bindir}/tcsdstarter
%{_unitdir}/%{_name}.service
%{_sysconfdir}/default/%{_name}
%{_unitdir}/tpm12-tpmbios.service
%{_unitdir}/tpm12-tpminit.service
%{_unitdir}/tpm12-tcsd.service


%pre
mkdir -p %{_datadir}

getent group tss >/dev/null || groupadd -g 62 -r tss
getent passwd tss >/dev/null || \
useradd -r -u 59 -g tss -d /dev/null -s /sbin/nologin \
 -c "Account used by the trousers package to sandbox the tcsd daemon" tss
exit 0

%post
%systemd_postun %{_name}.serivce
%systemd_postun simp-tpm12-tpmbios.service
%systemd_postun simp-tpm12-tpminit.service
%systemd_postun simp-tpm12-tcsd.service

%preun
%systemd_preun %{_name}.serivce
%systemd_preun simp-tpm12-tpmbios.service
%systemd_postun simp-tpm12-tpminit.service
%systemd_postun simp-tpm12-tcsd.service

%postun
%systemd_postun %{_name}.serivce
%systemd_postun simp-tpm12-tpmbios.service
%systemd_postun simp-tpm12-tpminit.service
%systemd_postun simp-tpm12-tcsd.service

%changelog
* Mon Jan 7 2019 Michael Morrone <michael.morrone@onyxpoint.com> - 0.0.1
- Initial commit
