# TODO
# - plugins build doesn't pass CFLAGS
Summary:	A next generation init replacement
Summary(pl):	Zamiennik inita nast�pnej generacji
Name:		initng
Version:	0.1.6
Release:	0.5
Epoch:		0
License:	GPL v2
Group:		Base
Source0:	http://initng.thinktux.net/download/%{name}-%{version}.tar.bz2
# Source0-md5:	06ae9e6453f1cc4e157140fdfa79ff38
Patch0:		%{name}-PLD.patch
Patch1:		%{name}-lib64.patch
Patch2:		%{name}-utmpx.patch
URL:		http://jw.dyndns.org/initng/
BuildRequires:	sed >= 4.0
BuildRequires:	/etc/pld-release
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
Initng ca�kowicie zast�puje stare i w wielu miejscach przestarza�e
narz�dzie SysVinit. Zosta� zaprojektowany z my�l� o szybko�ci, robi
r�wnolegle tak wiele jak tylko mo�liwe. Innymi s�owy: umo�liwia du�o
szybszy start systemu uniksowego oraz zapewnia wi�ksz� kontrol� i
statystyki.

# just temp place holder for those scripts
%package fixes
Summary:	initng experimental patches and fixes
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description fixes
contains fixes directory from initng distribution, which appear to
replace few system files. you should probably install this package
with --replacefiles rpm option.

%package initscripts
Summary:	Bundled initscripts
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description initscripts
this package contains the bundled iniscripts. these are very
gentooish. i plan to write new ones for pld using existing rc-scripts.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
#%patch2 -p1

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

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README AUTHORS ChangeLog NEWS TEMPLATE_HEADER TODO CODING_STANDARDS
%doc doc/databases.txt doc/imanual.txt doc/initng.txt
%doc doc/empty.conf doc/hard.conf
%doc doc/gentoo-chart.png doc/initng-chart.png
%dir %{_sysconfdir}
%dir %{_sysconfdir}/conf
%dir %{_sysconfdir}/daemon
%dir %{_sysconfdir}/debug
%dir %{_sysconfdir}/net
%dir %{_sysconfdir}/system
%dir %{_sysconfdir}/plugin
%dir %{_libdir}
%dir %{_libdir}/scripts
%dir %{_libdir}/scripts/net
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/plugin/readahead.i
%attr(755,root,root) /%{_lib}/libinitng.so.*.*.*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
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

%files initscripts
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/daemon/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/debug/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/system/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/net/*.i
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.runlevel
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf/test.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xmltest.xml
%attr(755,root,root) %{_sbindir}/gen_system_runlevel.sh
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
