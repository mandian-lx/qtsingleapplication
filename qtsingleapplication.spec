%define debug_package %nil
# Upstream uses weird versioning convention
%define upstreamver 2.6_1
%define version %(echo %upstreamver | sed 's!_!.!' )

%define major 1
%define libname %mklibname %{name} 2.6
%define libcore %mklibname qtsinglecoreapplication 2.6
%define devname %mklibname %{name} -d
%define devcore %mklibname qtsinglecoreapplication -d

Summary:	Qt library to start applications only once per user
Name:		qtsingleapplication
Version:	%{version}
Release:	14
Group:		Development/KDE and Qt
License:	GPLv3 or LGPLv2 with exceptions
Url:		http://qt.nokia.com/products/appdev/add-on-products/catalog/4/Utilities/qtsingleapplication
Source0:	http://get.qt.nokia.com/qt/solutions/lgpl/qtsingleapplication-%{upstreamver}-opensource.tar.gz
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
# gcc-4.7 compilation fix
Patch3:		qtsingleapplication-gcc47.patch

BuildRequires:	qt4-devel
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
%{_qt_libdir}/lib*SingleApplication*.so.%{major}*

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
%doc LGPL_EXCEPTION.txt LICENSE.* README.TXT
%doc doc examples
%{_qt_libdir}/lib*SingleApplication*.so
%dir %{_qt_includedir}/QtSolutions/
%{_qt_includedir}/QtSolutions/QtSingleApplication
%{_qt_includedir}/QtSolutions/%{name}.h
%{_qt_datadir}/mkspecs/features/%{name}.prf

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
%{_qt_libdir}/lib*SingleCoreApplication*.so.%{major}*

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
%doc LGPL_EXCEPTION.txt LICENSE.*
%{_qt_libdir}/lib*SingleCoreApplication*.so
%dir %{_qt_includedir}/QtSolutions/
%{_qt_includedir}/QtSolutions/QtSingleCoreApplication
%{_qt_includedir}/QtSolutions/qtsinglecoreapplication.h
%{_qt_datadir}/mkspecs/features/qtsinglecoreapplication.prf

#--------------------------------------------------------------------

%prep
%setup -qn %{name}-%{upstreamver}-opensource
%apply_patches

# (Fedora) We already disabled bundling this extrenal library.
# But just to make sure:
rm src/{QtLocked,qtlocked}*


%build
touch .licenseAccepted
# Does not use GNU configure
./configure -library
%qmake_qt4
%make

%install
# libraries
mkdir -p %{buildroot}%{_qt_libdir}
cp -a lib/* %{buildroot}%{_qt_libdir}
chmod 755 %{buildroot}%{_qt_libdir}/*.so.*.*.*

# headers
mkdir -p %{buildroot}%{_qt_includedir}/QtSolutions
cp -a \
    src/qtsingleapplication.h \
    src/QtSingleApplication \
    src/qtsinglecoreapplication.h \
    src/QtSingleCoreApplication \
    %{buildroot}%{_qt_includedir}/QtSolutions

mkdir -p %{buildroot}%{_qt_datadir}/mkspecs/features
cp -a %{SOURCE1} %{SOURCE2} %{buildroot}%{_qt_datadir}/mkspecs/features/

