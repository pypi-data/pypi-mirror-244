Name: libolecf
Version: 20231203
Release: 1
Summary: Library to access the Object Linking and Embedding (OLE) Compound File (CF) format
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libolecf
               
BuildRequires: gcc               

%description -n libolecf
Library to access the Object Linking and Embedding (OLE) Compound File (CF) format

%package -n libolecf-static
Summary: Library to access the Object Linking and Embedding (OLE) Compound File (CF) format
Group: Development/Libraries
Requires: libolecf = %{version}-%{release}

%description -n libolecf-static
Static library version of libolecf.

%package -n libolecf-devel
Summary: Header files and libraries for developing applications for libolecf
Group: Development/Libraries
Requires: libolecf = %{version}-%{release}

%description -n libolecf-devel
Header files and libraries for developing applications for libolecf.

%package -n libolecf-python3
Summary: Python 3 bindings for libolecf
Group: System Environment/Libraries
Requires: libolecf = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libolecf-python3
Python 3 bindings for libolecf

%package -n libolecf-tools
Summary: Several tools for reading Object Linking and Embedding (OLE) Compound Files (CF)
Group: Applications/System
Requires: libolecf = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libolecf-tools
Several tools for reading Object Linking and Embedding (OLE) Compound Files (CF)

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libolecf
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libolecf-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libolecf-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libolecf.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libolecf-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libolecf-tools
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sun Dec  3 2023 Joachim Metz <joachim.metz@gmail.com> 20231203-1
- Auto-generated

