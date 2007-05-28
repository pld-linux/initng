#define _rc RC1
#define	_snap 20051022
%define	_rel 0.1
Summary:	A next generation init replacement
Summary(de.UTF-8):	Init Skripts neuer Generation
Summary(pl.UTF-8):	Zamiennik inita następnej generacji
Name:		initng
Version:	0.6.10.1
Release:	%{?_snap:0.%{_snap}.}%{?_pre:0.%{_pre}.}%{_rel}
License:	GPL v2
Group:		Base
Source0:	http://download.initng.org/initng/v0.6/%{name}-%{version}.tar.bz2
# Source0-md5:	db8c66f51c6ed07f144df0de2d79a2cc
Patch0:		%{name}-savefile.patch
Patch1:		%{name}-utmpx.patch
Patch2:		%{name}-vserver.patch
Patch3:		%{name}-nokillia.patch
URL:		http://www.initng.org/
BuildRequires:	cmake
BuildRequires:	rpmbuild(macros) >= 1.293
BuildRequires:	sed >= 4.0
Requires(post):	/sbin/ldconfig
Requires(post):	/sbin/telinit
Conflicts:	initng-ifiles < 0.0.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_exec_prefix	/
%define		_sysconfdir		/etc/%{name}
%define		_libdir			/%{_lib}/%{name}
%define		_bindir			%{_prefix}/sbin
# this is to avoid ugly //sbin
%define		_sbindir		/sbin

%description
Initng is a full replacement of the old and in many ways deprecated
SysVinit tool. It is designed with speed in mind, doing as much as
possible asynchronously. In other words: It will boot your unix-system
much faster, and give you more control and statistics over your
system.

%description -l de.UTF-8
Initng ersätzt vollständig das doch schon sehr alte und veralterte
SysVinit. Es wurde mit dem Hintergedanken der Schnelligkeit
entwickelt, es macht so viel wie nur möglich parrallel. Mit anderen
Worten: Es bootet das Unixsystem viel schneller und gibt dir mehr
Kontrolle und Statistiken über das System.

%description -l pl.UTF-8
Initng całkowicie zastępuje stare i w wielu miejscach przestarzałe
narzędzie SysVinit. Został zaprojektowany z myślą o szybkości, robi
równolegle tak wiele jak tylko możliwe. Innymi słowy: umożliwia dużo
szybszy start systemu uniksowego oraz zapewnia większą kontrolę i
statystyki.

%package devel
Summary:	Header files for initng
Summary(de.UTF-8):	Header Dateien für initng
Summary(pl.UTF-8):	Pliki nagłówkowe initng
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
initng header files for developing plugins for initng.

%description devel -l de.UTF-8
Initng header Dateien zur Entwicklung neuer Plugins.

%description devel -l pl.UTF-8
Pliki nagłówkowe initng do tworzenia wtyczek dla initng.

%prep
%setup -q -n %{name}%{!?_snap:-%{version}}%{?_pre:_%{_pre}}%{?_rc}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%cmake . \
	-DCOUNT_ME=OFF \
	-DCMAKE_SKIP_RPATH=ON \
	-DLIB_INSTALL_DIR=/%{_lib}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# install test_parser program, which will help you check your .i files validity
install devtool/test_parser $RPM_BUILD_ROOT%{_sbindir}/%{name}-test_parser

# duplicated
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}
# should be in sysconfig probably
rm -f $RPM_BUILD_ROOT%{_libdir}/service_alias
rm -f $RPM_BUILD_ROOT/%{_lib}/libsngeclient.a
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/killall5-ignore

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
if [ "$1" = 1 ]; then
	%banner -e %{name} <<-EOF
Remember to add init=%{_sbindir}/initng in your grub or lilo config to use initng.

You should install 'initng-pld' for PLD Linux rc-scripts based scripts,
or 'initng-initscripts' for the original distributed scripts.

Happy testing.
EOF
fi

/sbin/telinit u || :

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README AUTHORS ChangeLog NEWS TODO
%doc doc/initng.txt
%doc doc/gentoo-chart.png doc/initng-chart.png
%dir %{_sysconfdir}
%dir %{_libdir}
%attr(755,root,root) /%{_lib}/libinitng.so.*.*.*
%attr(755,root,root) /%{_lib}/libngeclient.so.*.*.*
%attr(755,root,root) /%{_lib}/libngcclient.so.*.*.*
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_sbindir}/initng
%attr(755,root,root) %{_sbindir}/initng-test_parser
%attr(755,root,root) %{_sbindir}/initng-segfault
%attr(755,root,root) %{_sbindir}/ngc
%attr(755,root,root) %{_sbindir}/ngdc
%attr(755,root,root) %{_sbindir}/nghalt
%attr(755,root,root) %{_sbindir}/ngreboot
%attr(755,root,root) %{_sbindir}/ngrestart
%attr(755,root,root) %{_sbindir}/ngstart
%attr(755,root,root) %{_sbindir}/ngstatus
%attr(755,root,root) %{_sbindir}/ngstop
%attr(755,root,root) %{_sbindir}/ngzap
%attr(755,root,root) %{_sbindir}/nge
%attr(755,root,root) %{_sbindir}/nge_raw
%{_mandir}/man8/initng.8*
%{_mandir}/man8/ngc.8*
%{_mandir}/man8/ngdc.8*

%files devel
%defattr(644,root,root,755)
/%{_lib}/libngeclient.so
/%{_lib}/libngcclient.so
/%{_lib}/libinitng.so
%{_includedir}/initng
