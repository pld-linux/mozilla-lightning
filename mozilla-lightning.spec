# TODO
# - searches for nss-config; fails and builds with internal nss
#
# Conditional build:
%bcond_without	tests	# Disabling these tests can speed build time and reduce disk space considerably.
%bcond_without	gnome	# disable all GNOME components (gnomevfs, gnome, gnomeui)
#
Summary:	Mozilla Lightning - calendar extension for Thunderbird
Summary(pl.UTF-8):	Mozilla Lightning - kalendarz jako rozszerzenie dla Thunderbirda
Name:		mozilla-lightning
Version:	0.7
Release:	0.1
License:	MPL/GPL/LGPL
Group:		X11/Applications/Networking
#Source0:	http://releases.mozilla.org/pub/mozilla.org/calendar/lightning/releases/0.5/source/lightning-sunbird-%{version}-source.tar.bz2
Source0:	lightning-sunbird-%{version}-20071027-source.tar.bz2
# Source0-md5:	7bc573958c75630962a121d7ed12eb6f
URL:		http://www.mozilla.org/projects/calendar/lightning/
BuildRequires:	GConf2-devel >= 1.2.1
BuildRequires:	glib2-devel >= 1:1.3.7
BuildRequires:	gnome-vfs2-devel >= 2.0
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libgnome-devel >= 2.0
BuildRequires:	libgnomeui-devel >= 2.2.0
BuildRequires:	libjpeg-devel
BuildRequires:	nspr-devel >= 1:4.6.1-2
BuildRequires:	nss-devel >= 3.10.2
BuildRequires:	pango-devel >= 1:1.6.0
BuildRequires:	perl-modules
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

%description -l pl.UTF-8
Lightning udostępnia kalendarz Sunbird dla popularnego klienta poczty
elektronicznej Mozilla Thunderbird. Ponieważ jest to rozszerzenie,
Lightning jest ściśle zintegrowany z Thunderbirdem, co pozwala łatwo
wykonywać zadania kalendarzowe związane z pocztą elektroniczną.

%package lang-en
Summary:	English resources for Mozilla Lightning
Summary(pl.UTF-8):	Anglojęzyczne zasoby dla kalendarza Mozilla Lightning
Group:		X11/Applications/Networking
Requires(post,postun):	%{name} = %{version}-%{release}
Requires(post,postun):	textutils
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-lang-resources = %{version}-%{release}

%description lang-en
English resources for Mozilla Lightning.

%description lang-en -l pl.UTF-8
Anglojęzyczne zasoby dla kalendarza Mozilla Lightning.

%prep
%setup -qc

%build
cd mozilla

# info about lightning building: http://www.mozilla.org/projects/calendar/lightning/build.html
# general mozilla.org build notes: http://developer.mozilla.org/en/docs/Configuring_Build_Options
# To generate .mozconfig you may visit: http://webtools.mozilla.org/build/config.cgi
# more: http://www.mozilla.org/build/configurator-faq.html

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
%if %{?debug:1}0
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
ac_add_options --disable-optimize
%else
ac_add_options --disable-debug
ac_add_options --disable-debug-modules
ac_add_options --enable-optimize="%{rpmcflags}"
%endif
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-@CONFIG_GUESS@
ac_add_options --disable-freetype2
ac_add_options --disable-logging
ac_add_options --disable-old-abi-compat-wrappers
ac_add_options --enable-application=mail
ac_add_options --enable-default-toolkit=gtk2
ac_add_options --enable-extensions=default,lightning
ac_add_options --enable-image-decoders=all
ac_add_options --enable-image-encoders=all
ac_add_options --enable-ipcd
ac_add_options --enable-ldap-experimental
ac_add_options --enable-native-uconv
ac_add_options --enable-safe-browsing
ac_add_options --enable-storage
ac_add_options --enable-system-cairo
ac_add_options --enable-url-classifier
ac_add_options --enable-xft
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

%{__make} -j1 -f client.mk build \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
cd mozilla
install -d $RPM_BUILD_ROOT%{_thunderbirddir}/{extensions,chrome}
install obj-*/dist/xpi-stage/lightning.xpi $RPM_BUILD_ROOT%{_thunderbirddir}/extensions
install obj-*/dist/xpi-stage/lightning/chrome/lightning-en-US.jar $RPM_BUILD_ROOT%{_thunderbirddir}/chrome
install obj-*/dist/xpi-stage/lightning/chrome.manifest $RPM_BUILD_ROOT%{_thunderbirddir}/chrome/lightning-en-US.manifest

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_thunderbirddir}/extensions/lightning.xpi
# should put data there instead:
#%dir %{_thunderbirddir}/extensions/{e2fda1a4-762b-4020-b5ad-a41df1933103}

%files lang-en
%defattr(644,root,root,755)
%{_thunderbirddir}/chrome/lightning-en-US.jar
%{_thunderbirddir}/chrome/lightning-en-US.manifest
