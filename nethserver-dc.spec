Name:           nethserver-dc
Version: 1.0.3
Release: 1%{?dist}
Summary:        NethServer Domain Controller configuration

License:        GPLv3+
URL: %{url_prefix}/%{name}
Source0:        %{name}-%{version}.tar.gz
Source1:        ns-samba-1.0.0-1.ns7.x86_64.rpm

BuildRequires:  nethserver-devtools
BuildRequires:  systemd

Requires: nethserver-sssd, nethserver-release
Requires: expect
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Conflicts: nethserver-directory

%description
NethServer Samba 4 Domain Controller configuration

%prep
%setup

%build
%{makedocs}
perl createlinks

%install
rm -rf %{buildroot}
mkdir -p root/usr/lib/nethserver-dc
mv %{SOURCE1} root/usr/lib/nethserver-dc
(cd root   ; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} | \
  sed '\:^/etc/sysconfig/nsdc: d
\:^/etc/nethserver/todos.d/: d
\:^/etc/sudoers.d/: d
' > %{name}-%{version}-filelist

%post
%systemd_post nsdc.service

%preun
%systemd_preun nsdc.service

%postun
%systemd_postun


%files -f %{name}-%{version}-filelist
%doc COPYING
%doc README.rst
%dir %{_nseventsdir}/%{name}-update
%attr(0644,root,root) %config(noreplace) /etc/sysconfig/nsdc
%attr(0755,root,root) /etc/nethserver/todos.d/40nethserver-dc
%config %attr (0440,root,root) %{_sysconfdir}/sudoers.d/20_nethserver_dc

%changelog
* Mon Sep 12 2016 Davide Principi <davide.principi@nethesis.it> - 1.0.3-1
- Failures on Samba AD accounts management - Bug NethServer/dev#5103
- DC join failed, realmd cannot join this realm - Bug NethServer/dev#5099

* Thu Jul 21 2016 Davide Principi <davide.principi@nethesis.it> - 1.0.2-1
- LDAP bind on Samba 4 requires SSL (CVE-2016-2112) - NethServer/dev#5067

* Wed Jul 13 2016 Davide Principi <davide.principi@nethesis.it> - 1.0.1-1
- nethserver-dc backup fails if launched by cron or from interface -- NethServer/dev#5047

* Thu Jul 07 2016 Davide Principi <davide.principi@nethesis.it> - 1.0.0-1
- Release 1.0.0

* Tue May 17 2016 Davide Principi <davide.principi@nethesis.it> - 0.0.1
- Bump Samba 4.4.3

* Fri Jan 29 2016 Davide Principi <davide.principi@nethesis.it> - 0.0.0
- Initial version
