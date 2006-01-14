Summary:	A next generation init replacement
Summary(pl):	Zamiennik inita nastêpnej generacji
Name:		initng
Version:	0.5.2
#define	_snap 20051022
%define	_rel 0.1
Release:	%{?_snap:0.%{_snap}.}%{_rel}
License:	GPL v2
Group:		Base
#Source0:	/home/builder/svn/initng-20051022.tar.bz2
Source0:	http://initng.thinktux.net/download/v0.5/%{name}-%{version}.tar.bz2
# Source0-md5:	d28c1f8d5639a226bed28d5d713f17ac
Patch0:		%{name}-savefile.patch
Patch1:		%{name}-utmpx.patch
URL:		http://jw.dyndns.org/initng/
BuildRequires:	/etc/pld-release
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	sed >= 4.0
Requires:	bash
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_exec_prefix	/
%define		_sysconfdir		/etc/%{name}
%define		_libdir			/%{_lib}/%{name}

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
Summary(pl):	Eksperymentalne ³aty i poprawki do initng
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description fixes
Contains fixes directory from initng distribution, which appear to
replace few system files. You should probably install this package
with --replacefiles rpm option.

%description fixes -l pl
Ten pakiet zawiera katalog fixes z dystrybucji initng, który wydaje
siê zastêpowaæ niektóre pliki systemowe. Prawdopodobnie nale¿y
instalowaæ ten pakiet z opcj± rpm-a --replacefiles.

%package initscripts
Summary:	Bundled initscripts
Summary(pl):	Do³±czone skrypty inicjalizuj±ce
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description initscripts
This package contains the bundled iniscripts. These are very
gentooish. I plan to write new ones for PLD using existing rc-scripts.

%description initscripts -l pl
Ten pakiet zawiera do³±czone skrypty inicjalizuj±ce. S± bardzo
gentoowskie. Planowane jest napisanie nowych dlaPLD przy u¿yciu
istniej±cych rc-scripts.

%prep
%setup -q %{?_snap:-n %{name}}
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--%{?debug:en}%{!?debug:dis}able-debug \
	--sysconfdir=/etc \
	--libdir=/%{_lib} \
	--disable-install-init

#	--with-splash \
#	--with-splashy \

%{__make} \
	CPPFLAGS='-DINITNG_PLUGIN_DIR=\"/%{_lib}/%{name}\"'

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# install test_parser program, which will help you check your .i files
# validity
libtool --mode=install cp devtool/test_parser $RPM_BUILD_ROOT%{_sbindir}/%{name}-test_parser

# no devel package, so no devel files
rm -f $RPM_BUILD_ROOT/%{_lib}/libinitng.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# duplicated
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
if [ "$1" = 1 ]; then
	echo >&2 "Remember to add init=%{_sbindir}/initng in your grub or lilo config to use initng"
	echo >&2 "Happy testing."
fi

/sbin/ngc -c > /dev/null || :

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README AUTHORS ChangeLog NEWS TEMPLATE_HEADER TODO CODING_STANDARDS
%doc doc/imanual.txt doc/initng.txt
%doc doc/gentoo-chart.png doc/initng-chart.png
%dir %{_sysconfdir}
#%dir %{_sysconfdir}/conf
%dir %{_sysconfdir}/daemon
%dir %{_sysconfdir}/debug
%dir %{_sysconfdir}/net
%dir %{_sysconfdir}/system
#%dir %{_sysconfdir}/plugin
%dir %{_libdir}
%dir %{_libdir}/scripts
%dir %{_libdir}/scripts/net
#%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/plugin/readahead.i
%attr(755,root,root) /%{_lib}/libinitng.so.*.*.*
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_sbindir}/install_service
%attr(755,root,root) %{_sbindir}/initng
%attr(755,root,root) %{_sbindir}/initng-segfault
%attr(755,root,root) %{_sbindir}/initng-test_parser
%attr(755,root,root) %{_sbindir}/ng-update
%attr(755,root,root) %{_sbindir}/ngc
%attr(755,root,root) %{_sbindir}/ngdc
%attr(755,root,root) %{_sbindir}/system_off
%attr(755,root,root) %{_prefix}%{_sbindir}/ngcupdown
%{_mandir}/man8/initng.8*
%{_mandir}/man8/ngc.8*
%{_mandir}/man8/ng-update.8*
%{_mandir}/man8/gen_system_runlevel.8*
%{_mandir}/man8/ngdc.8*
%{_mandir}/man8/install_service.8*
%{_mandir}/man8/system_off.8*

%files fixes
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/pcmcia/network
%config(noreplace) %verify(not md5 mtime size) /etc/hotplug/net.agent
%attr(755,root,root) %{_prefix}%{_sbindir}/ifplugd.action
%attr(755,root,root) %{_prefix}%{_sbindir}/wpa_cli.action
/etc/ifplugd/action.d/ngcupdown

%files initscripts
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/killalli5
%dir %{_sysconfdir}/daemon/bluetooth
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/daemon/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/daemon/bluetooth/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/debug/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/system/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/net/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.runlevel
%config(noreplace) %verify(not md5 mtime size) %{_libdir}/service_alias
%attr(755,root,root) %{_sbindir}/gen_system_runlevel
%attr(755,root,root) %{_sbindir}/shutdown_script
%attr(755,root,root) %{_libdir}/scripts/net/dhclient-wrapper
%attr(755,root,root) %{_libdir}/scripts/net/dhcp
%attr(755,root,root) %{_libdir}/scripts/net/dhcpcd-backgrounder
%attr(755,root,root) %{_libdir}/scripts/net/essidnet
%attr(755,root,root) %{_libdir}/scripts/net/functions
%attr(755,root,root) %{_libdir}/scripts/net/gentoo-functions
%attr(755,root,root) %{_libdir}/scripts/net/ifconfig
%attr(755,root,root) %{_libdir}/scripts/net/interface
%attr(755,root,root) %{_libdir}/scripts/net/iproute2
%attr(755,root,root) %{_libdir}/scripts/net/iwconfig
%attr(755,root,root) %{_libdir}/scripts/net/system
%attr(755,root,root) %{_libdir}/scripts/net/udhcpc-wrapper
%attr(755,root,root) %{_libdir}/scripts/net/wpa_supplicant
%attr(755,root,root) %{_libdir}/scripts/net/wpa_cli.action
