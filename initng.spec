# TODO
# - plugins build doesn't pass CFLAGS
Summary:	A next generation init replacement
Summary(pl):	Zamiennik inita nastêpnej generacji
Name:		initng
Version:	0.1.3
Release:	0.6
Epoch:		0
License:	GPL v2
Group:		Base
Source0:	http://initng.thinktux.net/download/%{name}-%{version}.tar.bz2
# Source0-md5:	de9cb47d71792a1a9d47029549d0dfcc
Patch0:		%{name}-FHS.patch
Patch1:		%{name}-lib64.patch
URL:		http://jw.dyndns.org/initng/
BuildRequires:	sed >= 4.0
Requires:	bash
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_sbindir	/sbin
%define		_libdir		/%{_lib}/initng

%description
Initng is a full replacement of the old and in many ways deprecated
SysVinit tool. It is designed with speed in mind, doing as much as
possible asynchronously. In other words: It will boot your unix-system
much faster, and give you more control and statistics over your
system.

%description -l pl
Initng ca³kowicie zastêpuje stare i w wielu miejscach przestarza³e
narzêdzie SysVinit. Zosta³ zaprojektowany z my¶l± o szybko¶ci, robi
równolegle tak wiele jak tylko mo¿liwe. Innymi s³owy: umo¿liwia du¿o
szybszy start systemu uniksowego oraz zapewnia wiêksz± kontrolê i
statystyki.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

grep -rl '/lib/initng' . | xargs sed -i -e '
	s,\$(DESTDIR)/lib,$(DESTDIR)/%{_lib},g
	s,/lib/initng,/%{_lib}/initng,g
'

%build
%{__make} -C ngcontrol \
	CFLAGS='%{rpmcflags}' \
	LDFLAGS='%{rpmldflags}'

%{__make} -C src \
	CFLAGS='-DINITNG_PLUGIN_DIR=\"/%{_lib}/%{name}\" %{rpmcflags}' \
	LDFLAGS='%{rpmldflags}'

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	LIBDIR=%{_lib} \
	DESTDIR=$RPM_BUILD_ROOT

ln -sf libinitng.so.0.0 $RPM_BUILD_ROOT/%{_lib}/libinitng.so.0
ln -sf libinitng.so.0.0 $RPM_BUILD_ROOT/%{_lib}/libinitng.so
# TODO
rm -f $RPM_BUILD_ROOT/etc/hotplug/net.agent

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
	echo >&2 "Remember to add init=/sbin/initng in your grub or lilo config to use initng"
	echo >&2 "Happy testing."
fi

%files
%defattr(644,root,root,755)
%doc README AUTHORS ChangeLog NEWS TEMPLATE_HEADER TODO CODING_STANDARDS
%doc doc/databases.txt doc/empty.conf doc/hard.conf
%doc fixes/

#%config(noreplace) %verify(not md5 mtime size) /etc/hotplug/net.agent
%config(noreplace) %verify(not md5 mtime size) /etc/initng/plugin/readahead.i
%config(noreplace) %verify(not md5 mtime size) /etc/pcmcia/network

%dir %{_sysconfdir}
%dir %{_sysconfdir}/daemon
%dir %{_sysconfdir}/net
%dir %{_sysconfdir}/system
%dir %{_sysconfdir}/conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/daemon/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/system/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/net/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/system.runlevel
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/default.runlevel
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf/test.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/test.xml

%attr(755,root,root) /%{_lib}/libinitng.so
%attr(755,root,root) /%{_lib}/libinitng.so.0
%attr(755,root,root) /%{_lib}/libinitng.so.0.0
%dir %{_libdir}
%attr(755,root,root) %{_libdir}/libbashlaunch.so.*.*
%attr(755,root,root) %{_libdir}/libcpout.so.*.*
%attr(755,root,root) %{_libdir}/libezxmlparser.so.*.*
%attr(755,root,root) %{_libdir}/libinitctl.so.*.*
%attr(755,root,root) %{_libdir}/libiparser.so.*.*
%attr(755,root,root) %{_libdir}/libngc.so.*.*
%attr(755,root,root) %{_libdir}/libngc2.so.*.*
%attr(755,root,root) %{_libdir}/librlparser.so.*.*
%attr(755,root,root) %{_libdir}/libslaunch.so.*.*
%attr(755,root,root) %{_libdir}/libstdout.so.*.*
%attr(755,root,root) %{_libdir}/libup.so.*.*
%attr(755,root,root) %{_libdir}/libxmlconfig.so.*.*

%dir %{_libdir}/scripts
%dir %{_libdir}/scripts/net
%{_libdir}/scripts/net/dhclient-wrapper
%{_libdir}/scripts/net/dhcp
%{_libdir}/scripts/net/dhcpcd-backgrounder
%{_libdir}/scripts/net/essidnet
%{_libdir}/scripts/net/functions
%{_libdir}/scripts/net/gentoo-functions
%{_libdir}/scripts/net/ifconfig
%{_libdir}/scripts/net/interface
%{_libdir}/scripts/net/iproute2
%{_libdir}/scripts/net/iwconfig
%{_libdir}/scripts/net/system
%{_libdir}/scripts/net/udhcpc-wrapper
%{_libdir}/scripts/net/wpa_supplicant
%dir %{_libdir}/scripts/system
%{_libdir}/scripts/system/umount

%{_prefix}%{_sbindir}/ifplugd.action
%{_prefix}%{_sbindir}/wpa_cli.action

%attr(755,root,root) %{_sbindir}/initng
%attr(755,root,root) %{_sbindir}/ng-update
%attr(755,root,root) %{_sbindir}/ngc
%attr(755,root,root) %{_sbindir}/ngdc
%attr(755,root,root) %{_sbindir}/system_off

%{_mandir}/man8/initng.8*
%{_mandir}/man8/ngc.8*
