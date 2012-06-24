#
# Conditional build:
%bcond_with	tests	# enable tests (whatever they check)
%bcond_without	gnome	# disable all GNOME components (gnomevfs, gnome, gnomeui)
#
Summary:	Mozilla Lightning - calendar extension for Thunderbird
Summary(pl):	Mozilla Sunbird - samodzielny kalendarz
Name:		mozilla-lightning
Version:	0.3
Release:	0.1
License:	MPL/GPL/LGPL
Group:		X11/Applications/Networking
Source0:	http://releases.mozilla.org/pub/mozilla.org/calendar/lightning/releases/0.3/source/lightning-%{version}.source.tar.bz2
# Source0-md5:	8b2beb97f40d371993a175d53a1ef8ac
URL:		http://www.mozilla.org/projects/calendar/lightning/
BuildRequires:	GConf2-devel >= 1.2.1
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.0.0
BuildRequires:	freetype-devel
BuildRequires:	gnome-vfs2-devel >= 2.0
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	libgnome-devel >= 2.0
BuildRequires:	libgnomeui-devel >= 2.2.0
BuildRequires:	nspr-devel >= 1:4.6.1-2
BuildRequires:	nss-devel >= 3.10.2
BuildRequires:	pango-devel >= 1:1.6.0
BuildRequires:	perl-modules >= 5.004
BuildRequires:	pkgconfig
#BuildRequires:	xorg-lib-libXext-devel
#BuildRequires:	xorg-lib-libXft-devel >= 2.1
#BuildRequires:	xorg-lib-libXinerama-devel
#BuildRequires:	xorg-lib-libXp-devel
#BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	zip
BuildRequires:	zlib-devel >= 1.2.3
Requires:	mozilla-thunderbird >= 1.5
Requires:	nspr >= 1:4.6.1-2
Requires:	nss >= 3.10.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_thunderbirddir	%{_libdir}/mozilla-thunderbird

%description
Lightning brings the Sunbird calendar to the popular email client,
Mozilla Thunderbird. Since it's an extension, Lightning is tightly
integrated with Thunderbird, allowing it to easily perform
email-related calendaring tasks.

%description -l pl
Projekt Sunbird to wieloplatformowa aplikacja bed�ca samodzielnym
kalendarzem, oparta na j�zyku interfejsu u�ytkownika XUL.

%package devel
Summary:	Headers for developing programs that will use Mozilla Sunbird
Summary(pl):	Mozilla Sunbird - pliki nag��wkowe
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	nspr-devel >= 1:4.6.1-2
Obsoletes:	mozilla-devel

%description devel
Mozilla Sunbird development package.

%description devel -l pl
Pliki nag��wkowe kalendarza Mozilla Sunbird.

%package lang-en
Summary:	English resources for Mozilla Sunbird
Summary(pl):	Angloj�zyczne zasoby dla kalendarza Mozilla Sunbird
Group:		X11/Applications/Networking
Requires(post,postun):	%{name} = %{version}-%{release}
Requires(post,postun):	textutils
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-lang-resources = %{version}-%{release}

%description lang-en
English resources for Mozilla Sunbird.

%description lang-en -l pl
Angloj�zyczne zasoby dla kalendarza Mozilla Sunbird.

%prep
%setup -qc

%build
cd mozilla

# info about building: http://www.mozilla.org/projects/calendar/lightning/build.html
# To generate .mozconfig you may visit: http://webtools.mozilla.org/build/config.cgi

cat << 'EOF' > .mozconfig
# Options for 'configure' (same as command-line options).
ac_add_options --prefix=%{_prefix}
ac_add_options --exec-prefix=%{_exec_prefix}
ac_add_options --bindir=%{_bindir}
ac_add_options --sbindir=%{_sbindir}
ac_add_options --sysconfdir=%{_sysconfdir}
ac_add_options --datadir=%{_datadir}
ac_add_options --includedir=%{_includedir}
ac_add_options --libdir=%{_libdir}
ac_add_options --libexecdir=%{_libexecdir}
ac_add_options --localstatedir=%{_localstatedir}
ac_add_options --sharedstatedir=%{_sharedstatedir}
ac_add_options --mandir=%{_mandir}
ac_add_options --infodir=%{_infodir}
ac_add_options --enable-optimize="%{rpmcflags}"
%if %{?debug:1}0
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
%else
ac_add_options --disable-debug
ac_add_options --disable-debug-modules
%endif
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
ac_add_options --disable-logging
ac_add_options --enable-application=calendar
ac_add_options --enable-calendar
ac_add_options --enable-elf-dynstr-gc
ac_add_options --enable-image-decoders=all
ac_add_options --enable-image-encoders=all
ac_add_options --enable-ipcd
ac_add_options --enable-ldap-experimental
ac_add_options --enable-native-uconv
ac_add_options --enable-safe-browsing
ac_add_options --enable-storage
ac_add_options --enable-system-cairo
ac_add_options --enable-url-classifier
ac_add_options --with-default-mozilla-five-home=%{_thunderbirddir}
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-java-bin-path=/usr/bin
ac_add_options --with-java-include-path=/usr/include
ac_add_options --with-qtdir=/usr
ac_add_options --with-system-jpeg
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
EOF

%{__make} -f client.mk build \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C mozilla install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mozilla*
%attr(755,root,root) %{_bindir}/firefox
%attr(755,root,root) %{_sbindir}/*
%dir %{_thunderbirddir}
%{_thunderbirddir}/res
%dir %{_thunderbirddir}/components
%attr(755,root,root) %{_thunderbirddir}/components/*.so
%{_thunderbirddir}/components/*.js
%{_thunderbirddir}/components/*.xpt
%dir %{_thunderbirddir}/plugins
%attr(755,root,root) %{_thunderbirddir}/plugins/*.so
%{_thunderbirddir}/searchplugins
%{_thunderbirddir}/icons
%{_thunderbirddir}/defaults
%{_thunderbirddir}/greprefs
%dir %{_thunderbirddir}/extensions
%dir %{_thunderbirddir}/init.d
%attr(755,root,root) %{_thunderbirddir}/*.so
%attr(755,root,root) %{_thunderbirddir}/*.sh
%attr(755,root,root) %{_thunderbirddir}/m*
%attr(755,root,root) %{_thunderbirddir}/f*
%attr(755,root,root) %{_thunderbirddir}/reg*
%attr(755,root,root) %{_thunderbirddir}/x*
%{_pixmapsdir}/*
%{_desktopdir}/*

%dir %{_thunderbirddir}/chrome
%{_thunderbirddir}/chrome/*.jar
%{_thunderbirddir}/chrome/*.manifest
# -chat subpackage?
#%{_thunderbirddir}/chrome/chatzilla.jar
#%{_thunderbirddir}/chrome/content-packs.jar
%dir %{_thunderbirddir}/chrome/icons
%{_thunderbirddir}/chrome/icons/default

# -dom-inspector subpackage?
%dir %{_thunderbirddir}/extensions/inspector@mozilla.org
%{_thunderbirddir}/extensions/inspector@mozilla.org/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/regxpcom
%attr(755,root,root) %{_bindir}/xpidl
%attr(755,root,root) %{_bindir}/xpt_dump
%attr(755,root,root) %{_bindir}/xpt_link
%{_includedir}/%{name}
%{_pkgconfigdir}/*

%files lang-en
%defattr(644,root,root,755)
%{_thunderbirddir}/chrome/en-US.jar
%{_thunderbirddir}/chrome/en-US.manifest
