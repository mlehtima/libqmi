%global _hardened_build 1

Name:    libqmi
Summary: Support library to use the Qualcomm MSM Interface (QMI) protocol
Version: 1.32.0
Release: 1
License: LGPLv2+
URL:     http://freedesktop.org/software/libqmi
Source:  %{name}-%{version}.tar.bz2

BuildRequires: meson >= 0.53
BuildRequires: pkgconfig(glib-2.0) >= 2.56.0
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(gudev-1.0) >= 232
BuildRequires: pkgconfig(qrtr-glib)
BuildRequires: python3-base
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
%meson -Dgtk_doc=false -Dbash_completion=false -Dmbim_qmux=false -Dman=false
%meson_build

%install
%meson_install

mkdir -p %{buildroot}%{_datadir}/bash-completion
cp -a src/qmicli/qmicli %{buildroot}%{_datadir}/bash-completion

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING.LIB
%doc NEWS AUTHORS README.md
%{_libdir}/libqmi-glib.so.*
%{_libdir}/girepository-1.0/Qmi-1.0.typelib

%files devel
%{_includedir}/libqmi-glib/
%{_libdir}/pkgconfig/qmi-glib.pc
%{_libdir}/libqmi-glib.so
%{_datadir}/gir-1.0/Qmi-1.0.gir

%files utils
%license COPYING
%{_bindir}/qmicli
%{_bindir}/qmi-network
%{_bindir}/qmi-firmware-update
%{_datadir}/bash-completion
%{_libexecdir}/qmi-proxy
