# TODO
# - plugins build doesn't pass CFLAGS
Summary:	A next generation init replacement
Summary(pl):	Zamiennik inita nastêpnej generacji
Name:		initng
Version:	0.1.6
Release:	0.1
Epoch:		0
License:	GPL v2
Group:		Base
Source0:	http://initng.thinktux.net/download/%{name}-%{version}.tar.bz2
# Source0-md5:	06ae9e6453f1cc4e157140fdfa79ff38
Patch0:		%{name}-PLD.patch
Patch1:		%{name}-lib64.patch
URL:		http://jw.dyndns.org/initng/
BuildRequires:	sed >= 4.0
Requires:	bash
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix			/
%define		_sysconfdir		/etc/%{name}
%define		_libdir			/%{_lib}/%{name}
%define		_sbindir		/sbin
# for broken initng ac files prefix needs to be / and these redefined
%define		_datadir		/usr/share
%define		_docdir			%{_datadir}/doc
%define		_mandir			%{_datadir}/man

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

# just temp place holder for those scripts
%package fixes
Summary:	initng experimental patches and fixes
Group:		Base

%description fixes
contains fixes directory from initng distribution, which appear to
replace few system files. you should probably install this package
with --replacefiles rpm option.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

exit 0
grep -rl '/lib/initng' . | xargs sed -i -e '
	s,\$(DESTDIR)/lib,$(DESTDIR)/%{_lib},g
	s,/lib/initng,/%{_lib}/initng,g
'

%build
%configure \
	--sysconfdir=/etc \
	--libdir=/%{_lib} \

%{__make} \
	CFLAGS='-DINITNG_PLUGIN_DIR=\"/%{_lib}/%{name}\" %{rpmcflags}' \
	LDFLAGS='%{rpmldflags}'

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#DESTDIR=$RPM_BUILD_ROOT ./gen_system_runlevel.sh

# no devel package, so no devel files
rm -f $RPM_BUILD_ROOT/%{_lib}/libinitng.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# duplicated
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
	echo >&2 "Remember to add init=%{_sbindir}/initng in your grub or lilo config to use initng"
	echo >&2 "Happy testing."
fi

%files
%defattr(644,root,root,755)
%doc README AUTHORS ChangeLog NEWS TEMPLATE_HEADER TODO CODING_STANDARDS
%doc doc/databases.txt doc/imanual.txt doc/initng.txt
%doc doc/empty.conf doc/hard.conf
%doc doc/gentoo-chart.png doc/initng-chart.png

%config(noreplace) %verify(not md5 mtime size) /etc/initng/plugin/readahead.i

%dir %{_sysconfdir}
%dir %{_sysconfdir}/daemon
%dir %{_sysconfdir}/debug
%dir %{_sysconfdir}/net
%dir %{_sysconfdir}/system
%dir %{_sysconfdir}/conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/daemon/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/debug/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/system/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/net/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.runlevel
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf/test.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xmltest.xml

%attr(755,root,root) /%{_lib}/libinitng.so.*.*.*

%dir %{_libdir}
%attr(755,root,root) %{_libdir}/lib*.so.*.*

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

%attr(755,root,root) %{_sbindir}/gen_system_runlevel.sh
%attr(755,root,root) %{_sbindir}/install_service
%attr(755,root,root) %{_sbindir}/initng
%attr(755,root,root) %{_sbindir}/ng-update
%attr(755,root,root) %{_sbindir}/ngc
%attr(755,root,root) %{_sbindir}/ngdc
%attr(755,root,root) %{_sbindir}/system_off

%{_mandir}/man8/initng.8*
%{_mandir}/man8/ngc.8*
%{_mandir}/man8/ng-update.8*

%files fixes
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/pcmcia/network
%config(noreplace) %verify(not md5 mtime size) /etc/hotplug/net.agent
%attr(755,root,root) /usr/sbin/ifplugd.action
%attr(755,root,root) /usr/sbin/wpa_cli.action
