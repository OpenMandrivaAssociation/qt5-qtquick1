%define api %(echo %{version}|cut -d. -f1)
%define major %api
%define beta %nil

%define declarative %mklibname qt%{api}declarative %{api}
%define declaratived %mklibname qt%{api}declarative -d

%define _qt_prefix %{_libdir}/qt%{api}

# THIS PACKAGE DEPRECATED
Name:		qt5-qtquick1
Version:	5.7.1
%if "%{beta}" != ""
Release:	0.%{beta}.1
%define qttarballdir qt5-qtquick1-opensource-src-%{version}-%{beta}
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/submodules/%{qttarballdir}.tar.xz
%else
Release:	4
%define qttarballdir qt5-qtquick1-opensource-src-%{version}
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git clone git@github.com:qtproject/qtquick1.git && cd qtquick1
# git archive --prefix=qt5-qtquick1-opensource-src-5.7.1/ origin/5.7 | tar -x -C .. -f -
# cd ../qt5-qtquick1-opensource-src-5.7.1 && /usr/lib64/qt5/bin/syncqt.pl -version 5.7.1 && cd ..
# tar cfJ qt5-qtquick1-opensource-src-5.7.1.tar.xz qt5-qtquick1-opensource-src-5.7.1
Source0:	http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}.tar.xz
%endif
Source100:	%{name}.rpmlintrc
Summary:	QtQuick 1.x library
Group:		System/Libraries
License:	LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
URL:		http://www.qt.io
BuildRequires: 	pkgconfig(Qt5Core) >= %{version}
BuildRequires: 	qmake5 >= %{version}
BuildRequires: 	qt5-qtscript-private-devel >= %{version}
BuildRequires:	cmake(Qt5Designer)
BuildRequires:	pkgconfig(Qt5Network) >= %{version}
BuildRequires:	pkgconfig(Qt5Sql) >= %{version}
BuildRequires:	pkgconfig(Qt5Gui) >= %{version}
BuildRequires:	pkgconfig(Qt5Test) >= %{version}
BuildRequires: 	pkgconfig(Qt5Widgets) >= %{version}

%description
Support for the old QtQuick 1.x API.

%files
%{_qt_prefix}/bin/qml1plugindump
%{_qt_prefix}/bin/qmlviewer
%{_libdir}/qt5/imports
%{_libdir}/qt5/plugins/qml1tooling

#------------------------------------------------------------------------------

%package -n %{declarative}
Summary: Qt%{api} QtQuick 1.x Lib
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{declarative}
Qt%{api} QtQuick 1.x Lib.

%files -n %{declarative}
%{_qt5_libdir}/libQt5Declarative.so.%{api}*
%{_libdir}/qt5/plugins/designer/libqdeclarativeview.so

#------------------------------------------------------------------------------

%package -n %{declaratived}
Summary: Devel files needed to build apps based on QtQuick 1.x
Group:    Development/KDE and Qt
Requires: %{declarative} = %{EVRD}

%description -n %{declaratived}
Devel files needed to build apps based on QtQuick 1.x.

%files -n %{declaratived}
%_qt5_libdir/libQt5Declarative.prl
%_qt5_libdir/cmake/Qt5Declarative
%_qt5_includedir/QtDeclarative
%_qt5_libdir/pkgconfig/Qt5Declarative.pc
%_libdir/libQt5Declarative.so
%_qt_prefix/mkspecs/modules/qt_lib_declarative.pri
%_qt_prefix/mkspecs/modules/qt_lib_declarative_private.pri
%{_libdir}/cmake/Qt5Designer/Qt5Designer_QDeclarativeViewPlugin.cmake

#------------------------------------------------------------------------------

%package examples
Summary: Examples for QtQuick 1.x
Group: Development/KDE and Qt

%description examples
Examples for QtQuick 1.x.

%files examples
%{_libdir}/qt5/examples/declarative

#------------------------------------------------------------------------------

%prep
%setup -q -n %qttarballdir

%build
%qmake_qt5

#------------------------------------------------------------------------------
%make

%install
%makeinstall_std INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

# .la and .a files, die, die, die.
rm -f %{buildroot}%{_qt5_libdir}/lib*.la
rm -f %{buildroot}%{_qt5_libdir}/lib*.a
