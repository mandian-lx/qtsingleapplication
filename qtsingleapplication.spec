# Upstream uses weird versioning convention
%define upstreamver 2.6_1
%define version %(echo %upstreamver | sed 's!_!.!' )

%define libname_major 1
%define libname_core_major 1
%define libname %mklibname %name %libname_major
%define libname_core %mklibname qtsinglecoreapplication %libname_core_major
%define libname_devel %mklibname %name -d
%define libname_core_devel %mklibname qtsinglecoreapplication -d

Summary:	Qt library to start applications only once per user
Name:		qtsingleapplication
Version:	%{version}
Release:	1
Group:		Development/KDE and Qt
License:	GPLv3 or LGPLv2 with exceptions
URL:		http://qt.nokia.com/products/appdev/add-on-products/catalog/4/Utilities/qtsingleapplication
Source0:	http://get.qt.nokia.com/qt/solutions/lgpl/qtsingleapplication-%{upstreamver}-opensource.tar.gz
# (Fedora) The following source and 2 patches are sent upstream:
# http://bugreports.qt.nokia.com/browse/QTSOLBUG-119
# To add qmake support for convenience for packages using this library:
Source1:	qtsingleapplication.prf
Source2:	qtsinglecoreapplication.prf
# Don't build examples, Include qtsinglecoreapplication library in the build:
Patch0:		qtsingleapplication-build.diff
# (Fedora) The library includes a duplicate of qtlockedfile. We link to it dynamically instead:
Patch1:		qtsingleapplication-dont-bundle-external-libs.patch
# (Fedora) Additional API for building clementine
# http://bugreports.qt.nokia.com/browse/QTSOLBUG-133
Patch2:		qtsingleapplication-add-api.patch
BuildRequires:	qt4-devel
BuildRequires:	qtlockedfile-devel

%description
For some applications it is useful or even critical that they are started
only once by any user. Future attempts to start the application should
activate any already running instance, and possibly perform requested
actions, e.g. loading a file, in that instance.

The QtSingleApplication class provides an interface to detect a running
instance, and to send command strings to that instance.

%package	-n %libname
Summary:	Qt library to start applications only once per user
Group:		Development/KDE and Qt

%description	-n %libname
For some applications it is useful or even critical that they are started
only once by any user. Future attempts to start the application should
activate any already running instance, and possibly perform requested
actions, e.g. loading a file, in that instance.

The QtSingleApplication class provides an interface to detect a running
instance, and to send command strings to that instance.

This is the library package for QtSingleApplication.

%package	-n %libname_devel
Summary:	Development files for %{name}
Group:		Development/KDE and Qt
Requires:	%{libname} = %{version}-%{release}
Provides:	qtsingleapplication-devel = %{version}-%{release}

%description	-n %libname_devel
This package contains libraries and header files for developing applications
that use QtSingleApplication.

%package	-n %libname_core
Summary:	Qt library to start applications only once per user
Group:		Development/KDE and Qt

%description	-n %libname_core
For some applications it is useful or even critical that they are started
only once by any user. Future attempts to start the application should
activate any already running instance, and possibly perform requested
actions, e.g. loading a file, in that instance.

For console (non-GUI) applications, the QtSingleCoreApplication variant
is provided, which avoids dependency on QtGui.

This is the library package for QtSingleCoreApplication.

%package	-n %libname_core_devel
Summary:	Development files for qtsinglecoreapplication
Group:		Development/KDE and Qt
Requires:	%libname_core = %{version}-%{release}
Provides:	qtsinglecoreapplication-devel = %{version}-%{release}

%description -n %libname_core_devel
This package contains libraries and header files for developing applications
that use QtSingleCoreApplication.

%prep
%setup -q -n %{name}-%{upstreamver}-opensource
%patch0 -p1
%patch1 -p1
%patch2 -p1

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
mkdir -p %{buildroot}%{qt4lib}
cp -a lib/* %{buildroot}%{qt4lib}
chmod 755 %{buildroot}%{qt4lib}/*.so.*.*.*

# headers
mkdir -p %{buildroot}%{qt4include}/QtSolutions
cp -a \
    src/qtsingleapplication.h \
    src/QtSingleApplication \
    src/qtsinglecoreapplication.h \
    src/QtSingleCoreApplication \
    %{buildroot}%{qt4include}/QtSolutions

mkdir -p %{buildroot}%{qt4dir}/mkspecs/features
cp -a %{SOURCE1} %{SOURCE2} %{buildroot}%{qt4dir}/mkspecs/features/

%files -n %libname
%defattr(-,root,root,-)
%{qt4lib}/lib*SingleApplication*.so.%{libname_major}*

%files -n %libname_devel
%defattr(-,root,root,-)
%doc LGPL_EXCEPTION.txt LICENSE.* README.TXT
%doc doc examples
%{qt4lib}/lib*SingleApplication*.so
%dir %{qt4include}/QtSolutions/
%{qt4include}/QtSolutions/QtSingleApplication
%{qt4include}/QtSolutions/%{name}.h
%{qt4dir}/mkspecs/features/%{name}.prf

%files -n %libname_core
%defattr(-,root,root,-)
%{qt4lib}/lib*SingleCoreApplication*.so.%{libname_core_major}*

%files -n %libname_core_devel
%defattr(-,root,root,-)
%doc LGPL_EXCEPTION.txt LICENSE.*
%{qt4lib}/lib*SingleCoreApplication*.so
%dir %{qt4include}/QtSolutions/
%{qt4include}/QtSolutions/QtSingleCoreApplication
%{qt4include}/QtSolutions/qtsinglecoreapplication.h
%{qt4dir}/mkspecs/features/qtsinglecoreapplication.prf

