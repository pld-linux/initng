Summary:	A next generation init replacement
Name:		initng
Version:	0.0.10
Release:	0.1
Epoch:		0
License:	GPL v2
Group:		Base
Source0:	http://jw.dyndns.org/initng/%{name}-%{version}.tar.bz2
# Source0-md5:	fd4f633736dbf7c740f2f932131e349b
URL:		http://jw.dyndns.org/initng/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir /etc/%{name}
%define		_sbindir	/sbin

%description
Initng is a full replacement of the old and in many ways depricated
SysVinit tool. It is designed with speed in mind, doing as much as
possible asynchronously. In other words: It will boot your unix-system
much faster, and give you more control and statistics over your
system.

%prep
%setup -q

%build
%{__make} -C ngcontrol
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \

%{__make} -C src \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
	echo >&2 "Remember to add init=/sbin/initng in your grub or lilo config to use initng"
	echo >&2 "Happy testing."
fi

%files
%defattr(644,root,root,755)
%doc README AUTHORS ChangeLog NEWS TEMPLATE_HEADER TODO doc/databases.txt doc/empty.conf doc/hard.conf
%dir %{_sysconfdir}
%dir %{_sysconfdir}/daemon
%dir %{_sysconfdir}/system
%dir %{_sysconfdir}/net

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/daemon/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/system/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/net/*.i

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/system.runlevel
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/default.runlevel

%attr(755,root,root) %{_sbindir}/initng
%attr(755,root,root) %{_sbindir}/ng-update
%attr(755,root,root) %{_sbindir}/ngc
%attr(755,root,root) %{_sbindir}/ngdc
%attr(755,root,root) %{_sbindir}/pidfiledhack
%attr(755,root,root) %{_sbindir}/pidfilehack
%attr(755,root,root) %{_sbindir}/splash_update
%attr(755,root,root) %{_sbindir}/system_off
