Name:       popt
Summary:    C library for parsing command line parameters
Version:    1.16
Release:    1.1
Group:      System/Libraries
License:    MIT
URL:        http://www.rpm5.org/
Source0:    http://www.rpm5.org/files/%{name}/%{name}-%{version}.tar.gz
Source1001: packaging/popt.manifest 
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig


%description
Popt is a C library for parsing command line parameters. Popt was
heavily influenced by the getopt() and getopt_long() functions, but
it improves on them by allowing more powerful argument expansion.
Popt can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments. Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.



%package devel
Summary:    Development files for the popt library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
The popt-devel package includes header files and libraries necessary
for developing programs which use the popt C library. It contains the
API documentation of the popt library, too.



%prep
%setup -q -n %{name}-%{version}

%build
cp %{SOURCE1001} .

%configure --disable-static \
    --libdir=/%{_lib} \
    --disable-nls

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

# Move libpopt.{so,a} to %{_libdir}
rm -f $RPM_BUILD_ROOT/%{_lib}/libpopt.{la,so}
pushd $RPM_BUILD_ROOT/%{_lib}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
ln -sf ../../%{_lib}/$(ls libpopt.so.?.?.?) $RPM_BUILD_ROOT%{_libdir}/libpopt.so
popd

# Multiple popt configurations are possible
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/popt.d


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest popt.manifest
%defattr(-,root,root,-)
%doc COPYING
%{_sysconfdir}/popt.d
/%{_lib}/libpopt.so.*


%files devel
%manifest popt.manifest
%defattr(-,root,root,-)
%doc README
#%doc doxygen/html
%{_libdir}/libpopt.so
%{_libdir}/pkgconfig/popt.pc
%{_includedir}/popt.h
%doc %{_mandir}/man3/popt.3*
