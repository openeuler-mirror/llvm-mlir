Name:		llvm-mlir
Version:	12.0.1
Release:	0
Summary:	The MLIR project is a novel approach to building reusable and extensible compiler infrastructure.
License:	Apache 2.0
URL:		https://mlir.llvm.org/
Source0:	https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/llvm-project-%{version}.src.tar.xz
Patch0: 	0001-PATCH-mlir-Support-building-MLIR-standalone.patch
Patch1:		0002-PATCH-mlir-Fix-building-unittests-in-in-tree-build.patch

BuildRequires: gcc gcc-c++ cmake ninja-build zlib-devel python3-lit llvm-devel

%description
The MLIR project is a novel approach to building reusable and extensible compiler infrastructure. MLIR aims to address software fragmentation, improve compilation for heterogeneous hardware, significantly reduce the cost of building domain specific compilers, and aid in connecting existing compilers together.

%package static
Summary: MLIR static files
Requires: %{name} = %{version}

%description static
MLIR static files.

%package devel
Summary: MLIR development files
Requires: %{name} = %{version}-%{release}
Requires: %{name}-static = %{version}-%{release}

%description devel
MLIR development files.

%prep
%autosetup -n llvm-project-%{version}.src/mlir -p2
# remove all but keep mlir
find ../* -maxdepth 0 ! -name "mlir" -exec rm -rf {} +

%build
%cmake	-G Ninja \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_SKIP_RPATH=ON \
	-DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
	-DCMAKE_PREFIX_PATH=%{_libdir}/cmake/llvm/ \
	-DLLVM_BUILD_UTILS:BOOL=ON \
	-DMLIR_INCLUDE_DOCS:BOOL=ON \
	-DMLIR_INCLUDE_TESTS:BOOL=OFF \
	-DMLIR_INCLUDE_INTEGRATION_TESTS:BOOL=OFF \
	-DBUILD_SHARED_LIBS=OFF \
	-DLLVM_LIBDIR_SUFFIX=64 \
%ifarch %ix86 x86_64
	-DLLVM_TARGETS_TO_BUILD="X86"
%endif
%ifarch aarch64
	-DLLVM_TARGETS_TO_BUILD="AArch64"
%endif

%ninja_build

%install
%ninja_install

%check
# build process .exe tools normally use rpath or static linkage
%cmake_build --target check-mlir || true

%files
%license LICENSE.TXT
%{_libdir}/libMLIR*.so.*
%{_libdir}/libmlir_runner_utils.so.*
%{_libdir}/libmlir_c_runner_utils.so.*
%{_libdir}/libmlir_async_runtime.so.*

%files static
%{_libdir}/libMLIR*.a
%{_libdir}/libmlir_c_runner_utils_static.a

%files devel
%{_bindir}/mlir-tblgen
%{_libdir}/libMLIR*.so
%{_libdir}/libmlir_runner_utils.so
%{_libdir}/libmlir_c_runner_utils.so
%{_libdir}//libmlir_async_runtime.so
%{_includedir}/mlir	
%{_includedir}/mlir-c	
%{_libdir}/cmake/mlir

%changelog
* Wed Nov 16 2022 liyancheng <412998149@qq.com> - 12.0.1-0
- Type:Init
- ID:NA
- SUG:NA
- DESC:Init llvm-mlir repository
