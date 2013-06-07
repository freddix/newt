Summary:	Not Erik's Windowing Toolkit - text mode windowing with slang
Name:		newt
Version:	0.52.15
Release:	1
License:	LGPL
Group:		Libraries
Source0:	https://fedorahosted.org/releases/n/e/newt/%{name}-%{version}.tar.gz
# Source0-md5:	343ee3a0fd0eacdb7c508a1e1cfabf65
URL:		http://www.msg.com.mx/Newt/
BuildRequires:	autoconf
BuildRequires:	popt-devel
BuildRequires:	slang-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Newt is a windowing toolkit for text mode built from the slang
library. It allows color text mode applications to easily use
stackable windows, push buttons, check boxes, radio buttons, lists,
entry fields, labels, and displayable text. Scrollbars are supported,
and forms may be nested to provide extra functionality. This pacakge
contains the shared library for programs that have been built with
newt.

%package devel
Summary:	Developer's toolkit for newt windowing library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
These are the header files and libraries for developing applications
which use newt. Newt is a windowing toolkit for text mode, which
provides many widgets and stackable windows.

%package whiptail
Summary:	A dialog compliant program to build tty dialog boxes
Group:		Applications/Terminal

%description whiptail
Dialog compliant utility that allows you to build user interfaces in a
TTY (text mode only). You can call dialog from within a shell script
to ask the user questions or present with choices in a more user
friendly manner.

%prep
%setup -q

%build
%{__autoconf}
%configure \
	--with-gpm-support	\
	--without-python	\
	--without-tcl

%{__make} \
	PYTHONVERS=python%{py_ver}	\
	LIBTCL=				\
	SNACKSO=

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	PYTHONVERS=python%{py_ver}	\
	SNACKSO=			\
	WHIPTCLSO=			\
	instroot=$RPM_BUILD_ROOT	\
	libdir=%{_libdir}		\
	pythonbindir=%{py_sitedir}	\
	pythondir=%{py_sitedir}

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/bal

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/*.so.0.??
%attr(755,root,root) %{_libdir}/*.so.*.*

%files whiptail
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/whiptail

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*.h
%{_pkgconfigdir}/libnewt.pc

