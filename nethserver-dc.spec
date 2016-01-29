Name:           nethserver-dc
Version:        0.0.0
Release:        1%{?dist}
Summary:        NethServer Domain Controller configuration
BuildArch:      noarch

License:        GPLv3+
URL: %{url_prefix}/%{name}
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  nethserver-devtools
BuildRequires:  systemd

Requires: nethserver-lib, nethserver-release
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
NethServer Samba 4 Domain Controller configuration

%prep
%setup

%build
%{makedocs}
perl createlinks

%install
rm -rf %{buildroot}
(cd root   ; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} | \
  sed '\:/etc/sysconfig/nsdc: d' > %{name}-%{version}-filelist

%post
%systemd_post nsdc.service

%preun
%systemd_preun nsdc.service

%postun
%systemd_postun


%files -f %{name}-%{version}-filelist
%doc COPYING
%dir %{_nseventsdir}/%{name}-update
%attr(0644,root,root) %config(noreplace) /etc/sysconfig/nsdc

%changelog
* Fri Jan 29 2016 Davide Principi <davide.principi@nethesis.it>
- Initial version
