%define commit 1fca9c330d8548d84fccb66407fbaf3aae122d17
%define shortcommit %(c=%{commit}; echo ${c:0:7})

%define project_name qt-solutions

# Upstream uses weird versioning convention
%define upstreamver 2.6_1
%define version %(echo %upstreamver | sed 's!_!.!' )

%define major 1
%define libname %mklibname %{name} %{version}
%define libcore %mklibname qtsinglecoreapplication %{version}
%define devname %mklibname %{name} -d
%define devcore %mklibname qtsinglecoreapplication -d

Summary:	Qt library to start applications only once per user
Name:		qtsingleapplication
Version:	%{version}
Release:	15
Group:		Development/KDE and Qt
License:	BSD
Url:		https://github.com/qtproject/qt-solutions/
Source0:	https://github.com/qtproject/qt-solutions/archive/%{commit}/%{project_name}-%{commit}.tar.gz
# The following source and 2 patches are sent upstream:
# http://bugreports.qt.nokia.com/browse/QTSOLBUG-119
# To add qmake support for convenience for packages using this library:
Source1:	qtsingleapplication.prf
Source2:	qtsinglecoreapplication.prf

# Don't build examples, Include qtsinglecoreapplication library in the build:
Patch0:		qtsingleapplication-build.diff
# The library includes a duplicate of qtlockedfile. We link to it dynamically instead:
Patch1:		qtsingleapplication-dont-bundle-external-libs.patch
# Additional API for building clementine
# http://bugreports.qt.nokia.com/browse/QTSOLBUG-133
Patch2:		qtsingleapplication-add-api.patch

BuildRequires:	qt5-devel
BuildRequires:	qtlockedfile-devel

%description
For some applications it is useful or even critical that they are started
only once by any user. Future attempts to start the application should
activate any already running instance, and possibly perform requested
actions, e.g. loading a file, in that instance.

The QtSingleApplication class provides an interface to detect a running
instance, and to send command strings to that instance.

#--------------------------------------------------------------------

%package	-n %{libname}
Summary:	Qt library to start applications only once per user
Group:		Development/KDE and Qt

%description	-n %{libname}
For some applications it is useful or even critical that they are started
only once by any user. Future attempts to start the application should
activate any already running instance, and possibly perform requested
actions, e.g. loading a file, in that instance.

The QtSingleApplication class provides an interface to detect a running
instance, and to send command strings to that instance.

This is the library package for QtSingleApplication.

%files -n %{libname}
%{_qt5_libdir}/lib*SingleApplication*.so.%{major}*

#--------------------------------------------------------------------

%package	-n %{devname}
Summary:	Development files for %{name}
Group:		Development/KDE and Qt
Requires:	%{libname} = %{version}-%{release}
Provides:	qtsingleapplication-devel = %{version}-%{release}

%description	-n %{devname}
This package contains libraries and header files for developing applications
that use QtSingleApplication.

%files -n %{devname}
%doc README.TXT
%doc doc examples
%{_qt5_libdir}/lib*SingleApplication*.so
%dir %{_qt5_includedir}/QtSolutions/
%{_qt5_includedir}/QtSolutions/QtSingleApplication
%{_qt5_includedir}/QtSolutions/%{name}.h
%{_qt5_libdir}/qt5/mkspecs/features/%{name}.prf

#--------------------------------------------------------------------

%package	-n %{libcore}
Summary:	Qt library to start applications only once per user
Group:		Development/KDE and Qt

%description	-n %{libcore}
For some applications it is useful or even critical that they are started
only once by any user. Future attempts to start the application should
activate any already running instance, and possibly perform requested
actions, e.g. loading a file, in that instance.

For console (non-GUI) applications, the QtSingleCoreApplication variant
is provided, which avoids dependency on QtGui.

This is the library package for QtSingleCoreApplication.

%files -n %{libcore}
%{_qt5_libdir}/lib*SingleCoreApplication*.so.%{major}*

#--------------------------------------------------------------------

%package	-n %{devcore}
Summary:	Development files for qtsinglecoreapplication
Group:		Development/KDE and Qt
Requires:	%{libcore} = %{version}-%{release}
Provides:	qtsinglecoreapplication-devel = %{version}-%{release}

%description -n %{devcore}
This package contains libraries and header files for developing applications
that use QtSingleCoreApplication.

%files -n %{devcore}
%doc README.TXT
%{_qt5_libdir}/lib*SingleCoreApplication*.so
%dir %{_qt5_includedir}/QtSolutions/
%{_qt5_includedir}/QtSolutions/QtSingleCoreApplication
%{_qt5_includedir}/QtSolutions/qtsinglecoreapplication.h
%{_qt5_libdir}/qt5/mkspecs/features/qtsinglecoreapplication.prf

#--------------------------------------------------------------------

%prep
%setup -q -n %{project_name}-%{commit}/%{name}
%apply_patches

# (Fedora) We already disabled bundling this extrenal library.
# But just to make sure:
rm src/{QtLocked,qtlocked}*

# fix incoherent-version-in-name
sed -i -e 's|-head|-%{version}|g' common.pri

%build
# Accept license
touch .licenseAccepted

# Does not use GNU configure
./configure -library
%qmake_qt5
%make

%install
# libraries
install -dm 0755 %{buildroot}%{_qt5_libdir}/
cp -a lib/* %{buildroot}%{_qt5_libdir}/

# headers
install -dm 0755 %{buildroot}%{_qt5_includedir}/QtSolutions/
install -pm 0644 \
	src/QtSingleApplication \
	src/qtsingleapplication.h \
	src/QtSingleCoreApplication \
	src/qtsinglecoreapplication.h \
	%{buildroot}%{_qt5_includedir}/QtSolutions/

install -dm 0755 %{buildroot}%{_qt5_libdir}/qt5/mkspecs/features
install -pm 0644 %{SOURCE1} %{SOURCE2} %{buildroot}%{_qt5_libdir}/qt5/mkspecs/features/

