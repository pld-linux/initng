%define _rc RC1
#define	_snap 20051022
%define	_rel 0.6
Summary:	A next generation init replacement
Summary(pl):	Zamiennik inita nastêpnej generacji
Name:		initng
Version:	0.6.0
Release:	%{?_snap:0.%{_snap}.}%{?_pre:0.%{_pre}.}%{_rel}
License:	GPL v2
Group:		Base
Source0:	http://download.initng.thinktux.net/v0.6/%{name}-%{version}%{_rc}.tar.bz2
# Source0-md5:	4e29074adacaee1285e0f60fdc3a18c3
Patch0:		%{name}-savefile.patch
Patch1:		%{name}-utmpx.patch
Patch2:		%{name}-vserver.patch
URL:		http://initng.thinktux.net/
BuildRequires:	/etc/pld-release
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.194
BuildRequires:	sed >= 4.0
Requires(post):	/sbin/ldconfig
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

%description -l pl
Initng ca³kowicie zastêpuje stare i w wielu miejscach przestarza³e
narzêdzie SysVinit. Zosta³ zaprojektowany z my¶l± o szybko¶ci, robi
równolegle tak wiele jak tylko mo¿liwe. Innymi s³owy: umo¿liwia du¿o
szybszy start systemu uniksowego oraz zapewnia wiêksz± kontrolê i
statystyki.

%package devel
Summary:	Header files for initng
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
initng header files and libraries for developing plugins for initng.

%prep
%setup -q -n %{name}%{!?_snap:-%{version}}%{?_pre:_%{_pre}}%{?_rc}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--%{?debug:en}%{!?debug:dis}able-debug \
	--sysconfdir=/etc \
	--libdir=/%{_lib} \
	--disable-install-init \
	--disable-count-me

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# install test_parser program, which will help you check your .i files validity
libtool --mode=install cp devtool/test_parser $RPM_BUILD_ROOT%{_sbindir}/%{name}-test_parser
# duplicated
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}
# should be in sysconfig probably
rm -f $RPM_BUILD_ROOT%{_libdir}/service_alias
# bug probably
for a in ngdc nghalt ngreboot ngrestart ngstart ngstatus ngstop ngzap; do
	ln -sf ngc $RPM_BUILD_ROOT%{_sbindir}/$a
done

install src/initng_is.h $RPM_BUILD_ROOT%{_includedir}/initng

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

%{_sbindir}/ngc -c > /dev/null || :

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README AUTHORS ChangeLog NEWS TEMPLATE_HEADER TODO CODING_STANDARDS
%doc doc/initng.txt
%doc doc/gentoo-chart.png doc/initng-chart.png
%dir %{_sysconfdir}
%dir %{_libdir}
%attr(755,root,root) /%{_lib}/libinitng.so.*.*.*
%attr(755,root,root) /%{_lib}/libngeclient.so.*.*.*
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_sbindir}/initng
%attr(755,root,root) %{_sbindir}/initng-test_parser
%attr(755,root,root) %{_sbindir}/ngc
%attr(755,root,root) %{_sbindir}/ngdc
%attr(755,root,root) %{_sbindir}/nghalt
%attr(755,root,root) %{_sbindir}/ngreboot
%attr(755,root,root) %{_sbindir}/ngrestart
%attr(755,root,root) %{_sbindir}/ngstart
%attr(755,root,root) %{_sbindir}/ngstatus
%attr(755,root,root) %{_sbindir}/ngstop
%attr(755,root,root) %{_sbindir}/ngzap
%attr(755,root,root) %{_sbindir}/ngde
%attr(755,root,root) %{_sbindir}/nge
%attr(755,root,root) %{_sbindir}/nge_raw
%{_mandir}/man8/initng.8*
%{_mandir}/man8/ngc.8*
%{_mandir}/man8/ngdc.8*

%files devel
%defattr(644,root,root,755)
/%{_lib}/libngeclient.la
/%{_lib}/libngeclient.so
/%{_lib}/libinitng.la
/%{_lib}/libinitng.so
%{_libdir}/*.la
%{_includedir}/initng
