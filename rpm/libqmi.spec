%global _hardened_build 1

Name:    libqmi
Summary: Support library to use the Qualcomm MSM Interface (QMI) protocol
Version: 1.26.6
Release: 1%{?dist}
License: LGPLv2+
URL:     http://freedesktop.org/software/libqmi
Source:  %{name}-%{version}.tar.bz2

BuildRequires: gcc
BuildRequires: glib2-devel >= 2.32.0
BuildRequires: libgudev-devel >= 147
BuildRequires: python3-base
BuildRequires: autoconf-archive
#BuildRequires: libmbim-devel >= 1.18.0

%description
This package contains the libraries that make it easier to use QMI functionality
from applications that use glib.


%package devel
Summary: Header files for adding QMI support to applications that use glib
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: glib2-devel
Requires: pkgconfig

%description devel
This package contains the header and pkg-config files for development
applications using QMI functionality from applications that use glib.

%package utils
Summary: Utilities to use the QMI protocol from the command line
Requires: %{name}%{?_isa} = %{version}-%{release}
License: GPLv2+

%description utils
This package contains the utilities that make it easier to use QMI functionality
from the command line.


%prep
%autosetup -n %{name}-%{version}/%{name}

%build
%reconfigure --enable-qrtr --disable-static --disable-gtk-doc --disable-mbim-qmux --prefix=/usr

# Uses private copy of libtool:
# http://fedoraproject.org/wiki/Packaging:Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

LD_LIBRARY_PATH="$PWD/src/libqmi-glib/.libs" %make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc NEWS AUTHORS README
%license COPYING
%{_libdir}/libqmi-glib.so.*
%{_datadir}/bash-completion

%files devel
%dir %{_includedir}/libqmi-glib
%{_includedir}/libqmi-glib/*.h
%{_libdir}/pkgconfig/qmi-glib.pc
%{_libdir}/libqmi-glib.so

%files utils
%{_bindir}/qmicli
%{_bindir}/qmi-network
%{_bindir}/qmi-firmware-update
%{_mandir}/man1/*
%{_libexecdir}/qmi-proxy
