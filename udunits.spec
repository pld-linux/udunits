#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_without	tests		# unit tests execution
#
Summary:	Unidata package for units of physical quantities
Summary(pl.UTF-8):	Pakiet Unidata do jednostek wielkości fizycznych
Name:		udunits
Version:	2.2.26
Release:	1
License:	BSD
Group:		Libraries
Source0:	ftp://ftp.unidata.ucar.edu/pub/udunits/%{name}-%{version}.tar.gz
# Source0-md5:	5803837c6019236d24a9c9795cc8b462
Patch0:		%{name}-info.patch
URL:		https://www.unidata.ucar.edu/software/udunits/
BuildRequires:	CUnit
BuildRequires:	expat-devel >= 1.95
BuildRequires:	texinfo
Requires(post,postun):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The UDUNITS package supports units of physical quantities. Its C
library provides for arithmetic manipulation of units and for
conversion of numeric values between compatible units. The package
contains an extensive unit database, which is in XML format and
user-extendable. The package also contains a command-line utility for
investigating units and converting values.

%description -l pl.UTF-8
Pakiet UDUNITS obsługuje jednostki wielkości fizycznych. Biblioteka C
zapewnia operacje arytmetyczne na jednostkach oraz przeliczanie
wartości liczbowych międzi zgodnymi jednostkami. Pakiet zawiera
obszerną bazę danych jednostek w rozszerzalnym formacie XML. Zawiera
także narzędzie linii poleceń do badania jednostek i przeliczania
wartości.

%package devel
Summary:	Header files for UDUNITS-2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki UDUNITS-2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for UDUNITS-2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki UDUNITS-2.

%package static
Summary:	Static UDUNITS-2 library
Summary(pl.UTF-8):	Statyczna biblioteka UDUNITS-2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static UDUNITS-2 library.

%description static -l pl.UTF-8
Statyczna biblioteka UDUNITS-2.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/udunits

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc ANNOUNCEMENT BACKLOG CHANGE_LOG COPYRIGHT README
%attr(755,root,root) %{_bindir}/udunits2
%attr(755,root,root) %{_libdir}/libudunits2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libudunits2.so.0
%{_datadir}/udunits
%{_infodir}/udunits2prog.info*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libudunits2.so
%{_libdir}/libudunits2.la
%{_includedir}/converter.h
%{_includedir}/udunits.h
%{_includedir}/udunits2.h
%{_infodir}/udunits2.info*
%{_infodir}/udunits2lib.info*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libudunits2.a
%endif
