%define beta rc3

%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	Preprocessing, echo cancellation and jitter buffer helpers for Speex
Name:		speexdsp
Version:	1.2
Release:	0.%{beta}.1
License:	BSD
Group:		Sound
URL:		http://www.speex.org/
Source0:	http://downloads.us.xiph.org/releases/speex/%{name}-%{version}%{beta}.tar.gz

%description
Preprocessing, echo cancellation and jitter buffer helpers for Speex

Speex is a patent-free audio codec designed especially for voice (unlike 
Vorbis which targets general audio) signals and providing good narrowband 
and wideband quality. This project aims to be complementary to the Vorbis
codec.

%package -n	%{libname}
Summary:	Shared library of the Speex codec
Group:		System/Libraries

%description -n	%{libname}
This package contains the shared library required for running
applications based on Speex.

%package -n	%{develname}
Summary:	Speex development files
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname -s -d speex} < 1.2-0.rc1.7

%description -n	%{develname}
Speex development files.

%prep
%setup -qn %{name}-%{version}%{beta}

%build
autoreconf -fi
export CFLAGS='%{optflags} -DRELEASE'
%configure \
	--disable-static \
	--enable-binaries
%make

%install
%makeinstall_std

%files -n %{libname}
%{_libdir}/libspeexdsp.so.%{major}*

%files -n %{develname}
%doc %{_docdir}/speexdsp
%{_libdir}/libspeexdsp*.so
%{_includedir}/speex/*
%{_libdir}/pkgconfig/speexdsp.pc
