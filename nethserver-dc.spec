# Do not try to package empty debug_package
%global debug_package %{nil}

# Naming of 32bit arm is a mess..
%ifarch armv7hl
%define source1_arch armv7hl
%else
%define source1_arch %{_arch}
%endif

Name:           nethserver-dc
Version: 1.9.0
Release: 1%{?dist}
Summary:        NethServer Domain Controller configuration

License:        GPLv3+
URL: %{url_prefix}/%{name}
Source0:        %{name}-%{version}.tar.gz
Source1:        https://github.com/NethServer/ns-samba/releases/download/4.16.5/ns-samba-4.16.5-1.ns7.%{source1_arch}.rpm
Source2:        https://github.com/NethServer/ns-samba/releases/download/4.16.5/compat-gnutls37-3.7.2-1.el7.%{source1_arch}.rpm
Source3:        https://github.com/NethServer/ns-samba/releases/download/4.16.5/compat-nettle37-3.7.3-1.el7.%{source1_arch}.rpm
Source4:        https://github.com/NethServer/ns-samba/releases/download/4.16.5/gmp-6.1.2-1.el7.%{source1_arch}.rpm

BuildRequires:  nethserver-devtools
BuildRequires:  systemd

Requires: nethserver-sssd > 1.1.9-1.ns7
Requires: rsync
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
mv %{SOURCE2} root/usr/lib/nethserver-dc
mv %{SOURCE3} root/usr/lib/nethserver-dc
mv %{SOURCE4} root/usr/lib/nethserver-dc
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
%config %attr (0440,root,root) %{_sysconfdir}/sudoers.d/20_nethserver_dc

%changelog
* Mon Nov 14 2022 Davide Principi <davide.principi@nethesis.it> - 1.9.0-1
- Samba 4.16.5 (#112)
- Cannot login/join AD domain after Windows 11 22H2 update - Bug NethServer/dev#6702

* Tue Feb 15 2022 Davide Principi <davide.principi@nethesis.it> - 1.8.4-1
- Changing password with special chars fails for AD users - Bug NethServer/dev#6637

* Thu Jan 27 2022 Davide Principi <davide.principi@nethesis.it> - 1.8.3-1
- Password policy is not respected on samba AD clients - Bug NethServer/dev#6613

* Tue Apr 13 2021 Davide Principi <davide.principi@nethesis.it> - 1.8.2-1
- Windows NTP client time sync failed  - Bug NethServer/dev#6480

* Tue Apr 07 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.8.1-1
- Restore configuration without network override - NethServer/dev#6099

* Thu Feb 06 2020 Davide Principi <davide.principi@nethesis.it> - 1.8.0-1
- Samba DC 4.9.18 upgrade -- NethServer/dev#6046

* Tue Oct 01 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.7.0-1
- Samba DC 4.9.13 upgrade - NethServer/dev#5838

* Wed May 22 2019 Davide Principi <davide.principi@nethesis.it> - 1.6.6-1
- Bump Samba 4.8.12 -- NethServer/nethserver-dc#102

* Thu Apr 04 2019 Davide Principi <davide.principi@nethesis.it> - 1.6.5-1
- Sysvol ACLs not restored - Bug NethServer/dev#5733

* Thu Mar 14 2019 Davide Principi <davide.principi@nethesis.it> - 1.6.4-1
- DC down after bridge IP change - Bug NethServer/dev#5730

* Tue Feb 19 2019 Davide Principi <davide.principi@nethesis.it> - 1.6.3-1
- Bump Samba 4.8.9 -- NethServer/ns-samba#98

* Mon Dec 10 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.2-1
- Account expired cannot change password - Bug NethServer/dev#5670

* Fri Dec 07 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.1-1
- Detach user-cleanup event from user-delete - NethServer/dev#5624

* Mon Dec 03 2018 Davide Principi <davide.principi@nethesis.it> - 1.6.0-1
- Samba DC 4.8.6 upgrade - NethServer/dev#5633
- User management errors after disaster recovery - Bug NethServer/dev#5653

* Wed Oct 24 2018 Davide Principi <davide.principi@nethesis.it> - 1.5.7-1
- Fix sme8migration provision failure - NethServer/nethserver-dc#90
- Fix sme8migration provision failure - NethServer/nethserver-dc#89

* Fri Oct 05 2018 Davide Principi <davide.principi@nethesis.it> - 1.5.6-1
- Home user deletion - NethServer/dev#5594
- Avoid NSDC container full restart - NethServer/nethserver-dc#88

* Wed Sep 05 2018 Davide Principi <davide.principi@nethesis.it> - 1.5.5-1
- Bump ns-samba 4.7.10 -- NethServer/nethserver-dc#86

* Thu Aug 02 2018 Davide Principi <davide.principi@nethesis.it> - 1.5.4-1
- DC: randomly failed actions - Bug NethServer/dev#5544
- Added nsdc-run command

* Mon Jul 02 2018 Davide Principi <davide.principi@nethesis.it> - 1.5.3-1
- Send AD queries to a preferred DC - NethServer/dev#5534
- Template of krb5.conf - NethServer/dev#5535
- Bump ns-samba-4.7.8 - NethServer/nethserver-dc#83

* Wed Jun 13 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.2-1
- Migration from sme8: no bind credentials for applications - Bug NethServer/dev#5527

* Tue May 15 2018 Davide Principi <davide.principi@nethesis.it> - 1.5.1-1
- Wrong YUM repository config for NSDC upgrade procedure - Bug NethServer/dev#5495

* Thu Apr 26 2018 Davide Principi <davide.principi@nethesis.it> - 1.5.0-1
- Samba DC 4.7.7 upgrade - NethServer/dev#5457

* Thu Mar 29 2018 Davide Principi <davide.principi@nethesis.it> - 1.4.5-1
- Migration procedure from sme8 fails due to reserved account names - Bug NethServer/dev#5447

* Fri Mar 16 2018 Davide Principi <davide.principi@nethesis.it> - 1.4.4-1
- Security release of ns-samba 4.6.16 - Bug NethServer/dev#5436 

* Mon Mar 12 2018 Davide Principi <davide.principi@nethesis.it> - 1.4.3-1
- Locked in network interface rename page - Bug NethServer/dev#5428

* Tue Jan 23 2018 Davide Principi <davide.principi@nethesis.it> - 1.4.2-1
- Automatic update of AD LDAP credentials failed - Bug NethServer/dev#5413

* Wed Jan 10 2018 Davide Principi <davide.principi@nethesis.it> - 1.4.1-1
- AD access for LDAP simple auth applications - NethServer/dev#5396

* Tue Dec 12 2017 Davide Principi <davide.principi@nethesis.it> - 1.4.0-1
- Change the shell access after the user creation with SAMBA4 AD - NethServer/dev#5391

* Tue Dec 05 2017 Davide Principi <davide.principi@nethesis.it> - 1.3.3-1
- Bump ns-samba-4.6.11 CVE-2017-14746 - NethServer/nethserver-dc#70
- Automated RPM builds - NethServer/dev#5393 

* Fri Nov 24 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.3.2-1
- Cannot contact any KDC for realm (sssd) - Bug NethServer/dev#5382

* Mon Nov 06 2017 Davide Principi <davide.principi@nethesis.it> - 1.3.1-1
- Minimize nsdc update downtime - NethServer/dev#5372

* Mon Oct 16 2017 Davide Principi <davide.principi@nethesis.it> - 1.3.0-1
- Samba automatic updates - NethServer/dev#5360

* Thu Jul 20 2017 Davide Principi <davide.principi@nethesis.it> - 1.2.6-1
- Web interface for changing nsdc IP address - NethServer/dev#5330

* Thu Jul 06 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.5-1
- Cannot connect DC sysvol share on gateway - Bug NethServer/dev#5321
- Upgrade to Samba 4.6.5

* Thu Jun 08 2017 Davide Principi <davide.principi@nethesis.it> - 1.2.4-1
- Realm join fails with poor entropy - Bug NethServer/dev#5308

* Thu May 25 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.3-1
- Migrate LogonDrive prop - Bug NethServer/dev#5290
- Upgrade ns-samba to 4.6.4 (CVE-2017-7494)

* Mon May 22 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.2-1
- Unable to validate Samba domain password - Bug NethServer/dev#5289
- Default userPrincipalName is not an email address - Bug NethServer/dev#5284

* Wed May 10 2017 Davide Principi <davide.principi@nethesis.it> - 1.2.1-1
- Fix home dirs migration
- Accounts provider guided configuration - NethServer/dev#5253
- DC: container upgrade procedure - NethServer/dev#5251
- DC: add NTP server support - NethServer/dev#5249
- DC: allow changing container IP - NethServer/dev#5248
- Upgrade from NS 6 via backup and restore - NethServer/dev#5234

* Wed May 10 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.0-1
- Accounts provider guided configuration - NethServer/dev#5253
- DC: container upgrade procedure - NethServer/dev#5251
- DC: add NTP server support - NethServer/dev#5249
- DC: allow changing container IP - NethServer/dev#5248
- Upgrade from NS 6 via backup and restore - NethServer/dev#5234

* Mon Mar 06 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.3-1
- Migration from sme8 - NethServer/dev#5196

* Mon Feb 20 2017 Davide Principi <davide.principi@nethesis.it> - 1.1.2-1
- AD local provider: annoying task completed with errors notification - Bug NethServer/dev#5220

* Mon Jan 16 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.1-1
- DC: restore configuration fails - Bug NethServer/dev#5188

* Thu Dec 15 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.0-1
- Set the members of administrators group - NethServer/dev#5168
- Store locally AD credentials - NethServer/dev#5165
- Default "admins" config DB record - NethServer/dev#5157

* Mon Oct 17 2016 Davide Principi <davide.principi@nethesis.it> - 1.0.7-1
- Display NetBIOS domain name on DC configuration page - NethServer/dev#5124

* Mon Oct 10 2016 Davide Principi <davide.principi@nethesis.it> - 1.0.6-1
- Controller provisioning fails with long domain name - Bug NethServer/dev#5116

* Thu Sep 22 2016 Davide Principi <davide.principi@nethesis.it> - 1.0.5-1
- Nsdc domain join fails with long hostname - Bug NethServer/dev#5110

* Mon Sep 12 2016 Davide Principi <davide.principi@nethesis.it> - 1.0.4-1
- Failure on empty group creation - Bug NethServer/dev#5105

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
